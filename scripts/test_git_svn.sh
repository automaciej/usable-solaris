#!/bin/bash
#
# Written by Maciej Bliziński, 2011-01-06.
# $Id$
#
# This script reproduces an interesting scenario in which one code
# conflict in git-svn becomes ever-returning and eternal.
#
# This is a scenario in which there are 3 repositories:
#
# - The original svn repository (SVN_REPO)
# - git-svn clone of it (GIT_REPO_1)
# - git clone of the first git repository (GIT_REPO_2)
#
# Imagine a setup in which GIT_REPO_1 is used on a remote server, to
# which there's sometimes no access.  GIT_REPO_2 would be clone to
# a local machine, let's say a laptop, on which you work without
# internet access.  When you're done, you're pushing changes from
# GIT_REPO_2 to GIT_REPO_1, and finally 'git svn dcommit' to send the
# new code to your svn repository.

set -e
set -u
set -x

BASE=$(pwd)

declare -r SVN_REPO="${BASE}/svn-repo"
declare -r SVN_LOCAL="${BASE}/svn-local"
declare -r GIT_REPO_1="${BASE}/git-repo-1"
declare -r GIT_REPO_2="${BASE}/git-repo-2"

function git_edit_line {
  local number=$1
  local f=$2
  local postfix=$3
  echo "Editing line ${number} in git"
  cp "${f}" "${f}.bak"
  sed -i -e "s/line ${number}\$/line ${number} was modified - $postfix/" "${f}"
  git add "${f}"
  git diff --cached
  git commit -m "Modifying line ${number} in git"
}

echo "Removing previous directories"
rm -rf "${SVN_REPO}" "${GIT_REPO_1}" "${SVN_LOCAL}" "${GIT_REPO_2}"

svnadmin create "${SVN_REPO}"
svn co "file://${SVN_REPO}" "${SVN_LOCAL}"
pushd "${SVN_LOCAL}"
echo "An example text file" > foo.txt
counter=0
while [[ "${counter}" -lt 16 ]]
do
	echo "line ${counter}" >> foo.txt
	counter=$(( ${counter} + 1 ))
done
svn add foo.txt
svn ci -m "Initial commit" foo.txt
popd

# A clone/checkout of the svn repository into git
git svn clone "file://${SVN_REPO}" "${GIT_REPO_1}"
# A clone of the first git repository.
git clone "file://${GIT_REPO_1}" "${GIT_REPO_2}"

# Modification of line 2 of foo.txt in subversion.
pushd "${SVN_LOCAL}"
cp "foo.txt" "foo.txt.bak"
sed -i -e "s/line 2\$/line 2 was modified - in svn/" "foo.txt"
svn ci -m "Line 2 edited in subversion" "foo.txt"
popd

# A conflicting modification of line 2 of foo.txt in git.
pushd "${GIT_REPO_2}"
git_edit_line 2 foo.txt repo2
popd

# Merge from GIT_REPO_2 to GIT_REPO_1
pushd "${GIT_REPO_1}"
git remote add "repo-2" "file://${GIT_REPO_2}"
git pull "repo-2" master
git svn fetch
git svn rebase || true
# We have a conflict in foo.txt right now.
cat foo.txt
# <<<<<<< HEAD
# line 2 was modified - in svn
# =======
# line 2 was modified - repo2
# >>>>>>> Modifying line 2

# Resolving the code conflict.
patch -p 1 <<EOF
--- git-repo-1/foo.txt.bak	2011-01-05 20:42:45.000000000 +0000
+++ git-repo-1/foo.txt	2011-01-05 20:42:58.000000000 +0000
@@ -1,11 +1,7 @@
 An example text file
 line 0
 line 1
-<<<<<<< HEAD
-line 2 was modified - in svn
-=======
-line 2 was modified - repo2
->>>>>>> Modifying line 2 in git
+line 2 was modified - in svn and in repo2
 line 3
 line 4
 line 5
EOF
git add foo.txt
git commit -m "Resolved a conflict in foo.txt"
# git rebase --continue fails, because the merge is a no-op, annoying,
# but I can put up with it.
git rebase --continue || true
# This (--skip) works
git rebase --skip
# Calling git svn rebase the second time, to finish the rebase
git svn rebase
git svn dcommit
popd

# We've resolved the conflict, now it's the time to propagate the
# resolution to GIT_REPO_2.

pushd "${GIT_REPO_2}"
# git pull origin master fails because of the previous conflict
git pull origin master || true
cp "foo.txt" "foo.txt.bak"
# There's a sha1 in the file which we need to remove to be able to apply
# a patch.
sed -e 's/[0-9a-f]\{40\}/sha1/' -i foo.txt
patch <<EOF
--- foo.txt.bak	2011-01-05 21:01:32.000000000 +0000
+++ foo.txt	2011-01-05 21:01:44.000000000 +0000
@@ -1,11 +1,7 @@
 An example text file
 line 0
 line 1
-<<<<<<< HEAD
-line 2 was modified - repo2
-=======
 line 2 was modified - in svn and in repo2
->>>>>>> sha1
 line 3
 line 4
 line 5
EOF
git add foo.txt
git commit -m "Resolved a conflict when merging into repo2."
popd

# Pulling the resolution from repo2 to repo1.
pushd "${GIT_REPO_1}"
git pull "repo-2" master
popd

# At this point, foo.txt looks the same in all three SVN_REPO,
# GIT_REPO_1 and GIT_REPO_2.

# Time to do some more work on the plane.
# Editing a line unrelated to line 2.
pushd "${GIT_REPO_2}"
git_edit_line 10 foo.txt repo2
popd

# Pushing the change from GIT_REPO_2 to SVN_REPO via GIT_REPO_1
pushd "${GIT_REPO_1}"
git pull "repo-2" master
# We have successfully merged the second change from repo-2, which is in line
# 10 and does not conflict with changes in Subversion.
git svn fetch
# git svn rebase fails -- why?  This conflict has been resolved already.
# If you resolve the conflict by hand, it becomes a no-op, and you can't git
# rebase --continue.  Instead, you have git rebase --skip.
#
# The worst problem is that _every_ commt in repo-2 now results in the same code
# conflict appearing over and over again.
git svn rebase
git svn dcommit
popd
(cd "${GIT_REPO_1}"; gitk)
