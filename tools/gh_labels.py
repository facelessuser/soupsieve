"""Populate github labes for issue tracker."""
from github import Github
from collections import namedtuple
import sys
import os

# Repository name
REPO_NAME = 'soupsieve'

# Options
DELETE_SKIPPED = True

# Colors
BUG = 'c45b46'
FEATURE = '7b17d8'
SUPPORT = 'efbe62'
DOCS = 'b2ffeb'

CORE = '0b02e1'
AUX1 = '709ad8'

GENERAL = 'bfd4f2'

PENDING = 'f0f49a'
REJECTED = 'f7c7be'
APPROVED = 'beed6d'

LOW = 'dddddd'

# Lables.
# To rename a label, use ('old_name', 'new_name') as the key.
label_list = {
    # Issue type
    'bug': (BUG, "Bug report."),
    'feature': (FEATURE, "Feature request."),
    'support': (SUPPORT, "Support request."),

    # Category
    'API': (CORE, "Related to the API"),
    'selectors': (AUX1, "Related to selector implementations"),
    'docs': (DOCS, "Related to documentation."),

    # Sub categories
    'css-level-1': (GENERAL, "CSS level 1 selectors."),
    'css-level-2': (GENERAL, "CSS level 2 selectors."),
    'css-level-3': (GENERAL, "CSS level 3 selectors."),
    'css-level-4': (GENERAL, "CSS level 4 selectors."),
    'css-level-5': (GENERAL, "CSS level 5 selectors."),
    'css-custom': (GENERAL, "CSS custom selectors."),

    # Issue status
    'more-info-needed': (PENDING, "More information is required."),
    'needs-confirmation': (PENDING, "The alleged behavior needs to be confirmed."),
    'needs-decision': (PENDING, "A decision needs to be made regarding request."),
    'confirmed': (APPROVED, "Confirmed bug report or approved feature request."),
    'maybe': (LOW, "Pending approval of low priority request."),
    'duplicate': (REJECTED, "The issue has been previously reported."),
    'wontfix': (REJECTED, "The issue will not be fixed for the stated reasons."),
    'invalid': (REJECTED, "Invalid report (user error, upstream issue, etc)."),

    # Pull request status
    'work-in-progress': (PENDING, "A partial solution. More changes will be coming."),
    'needs-review': (PENDING, "Needs to be reviewed and/or approved."),
    'requires-changes': (PENDING, "Awaiting updates after a review."),
    'approved': (APPROVED, "The pull request is ready to be merged."),
    'rejected': (REJECTED, "The pull request is rejected for the stated reasons.")
}


# Label handling
class LabelEdit(namedtuple('LabelEdit', ['old', 'new', 'color', 'description', 'edit'])):
    """Label Edit tuple."""


def find_label(label, label_color, label_description):
    """Find label."""
    edit = None
    for name, values in label_list.items():
        color, description = values
        if isinstance(name, tuple):
            old_name = name[0]
            new_name = name[1]
        else:
            old_name = name
            new_name = name
        if label.lower() == old_name.lower():
            if new_name != label or color != label_color or label_description != description:
                edit = LabelEdit(old_name, new_name, color, description, True)
            else:
                edit = LabelEdit(old_name, new_name, color, description, False)
            break
    return edit


def update_labels(repo):
    """Update labels."""
    updated = set()
    for label in repo.get_labels():
        edit = find_label(label.name, label.color, label.description)
        if edit is not None and edit.edit:
            print(
                "    Updating '%s'='%s' -> '%s'='%s'" % (
                    label.name, label.color,
                    edit.new, edit.color
                )
            )
            label.edit(edit.new, edit.color, edit.description)
            updated.add(edit.old)
            updated.add(edit.new)
        elif edit is not None and not edit.edit:
            print("    Up to Date '%s'='%s'" % (label.name, label.color))
            updated.add(label.name)
        else:
            if DELETE_SKIPPED:
                print("    Deleting '%s'='%s'" % (label.name, label.color))
                label.delete()
            else:
                print("    Skipping '%s'='%s'" % (label.name, label.color))
            updated.add(label.name)
    for name, values in label_list.items():
        color, description = values
        if isinstance(name, tuple):
            new_name = name[1]
        else:
            new_name = name
        if new_name not in updated:
            print("    Creating '%s'='%s'" % (new_name, color))
            repo.create_label(new_name, color, description)


# Authentication
def get_auth():
    """Get authentication."""
    import getpass
    user = input("User Name:")  # noqa
    pswd = getpass.getpass('Password:')
    return Github(user, pswd)


def main():
    """Main."""

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        try:
            with open(sys.argv[1], 'r') as f:
                user_name, password = f.read().strip().split(':')
            git = Github(user_name, password)
            password = None
        except Exception:
            git = get_auth()
    else:
        git = get_auth()

    user = git.get_user()

    print('Finding repos...')
    for repo in user.get_repos():
        if repo.owner.name == user.name:
            if repo.name == REPO_NAME:
                print(repo.name)
                update_labels(repo)
                break


if __name__ == "__main__":
    main()
