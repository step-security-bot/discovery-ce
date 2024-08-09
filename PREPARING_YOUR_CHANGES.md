# Preparing Your Changes

This document contains information related to preparing changes for a pull request. Here's a quick checklist for a good PR, more details below:

1. A discussion around the change on [GitHub Discussions](https://github.com/0bytes-security/discovery-ce/discussions/) or in an issue.
1. A GitHub Issue with a good description associated with the PR
1. One feature/change per PR
1. One commit per PR
1. PR rebased on main (git rebase, not git pull)
1. Good descriptive commit message, with link to issue
1. No changes to code not directly related to your PR
1. Includes functional/integration test
1. Includes documentation

## Commit Message Format

We follow the **Conventional Commits** specification to ensure that commit messages are structured and consistent. The format for commit messages is as follows:

```text
<type>(<scope>): <subject>

<body>
```

- **type**: Specifies the nature of the commit. Common types include:
  - `feat`: A new feature for the user.
  - `fix`: A bug fix.
  - `docs`: Documentation only changes.
  - `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.).
  - `refactor`: A code change that neither fixes a bug nor adds a feature.
  - `perf`: A code change that improves performance.
  - `test`: Adding missing or correcting existing tests.
  - `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm).
  - `ci`: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs).
  - `chore`: Other changes that don't modify src or test files.
  - `revert`: Reverts a previous commit.

- **scope**: Optional, specifies the section of the codebase affected (e.g., `api`, `ui`, `database`). Use a lowercase word that clearly describes the area impacted by the change.

- **subject**: A brief description of the change. This should be written in the imperative mood (e.g., "fix bug" rather than "fixed bug" or "fixes bug").

### Description

If the commit has an out-sized impact relative to other commits, provide a detailed description in the body of the commit message. This should explain what changed, why it was necessary, and any implications for the project. 

### Example

```text
feat(api): add user authentication via OAuth

- Integrated OAuth 2.0 for secure user authentication
- Updated user model to include OAuth provider info
- Refactored existing authentication methods to support OAuth flow
```

Reviewers may ask you to amend your commits if they do not follow this structure or are not descriptive enough.

## Squashed Commits

We require that you squash all changes to a single commit. You can do this with the `git rebase -i HEAD~X` command where X is the number of commits you want to squash. See the [Git Documentation](https://git-scm.com/book/en/v2/Git-Branching-Rebasing) for more details.

## Developer's Certificate of Origin

Any contributions to Discovery must only contain code that can legally be contributed to Discovery, and which the Discovery project can distribute under its license.

Prior to contributing to Discovery please read the [Developer's Certificate of Origin](https://developercertificate.org/) and sign-off all commits with the `--signoff` option provided by `git commit`. For example:

```
git commit --signoff --message "This is the commit message"
```

This option adds a `Signed-off-by` trailer at the end of the commit log message.

## DCO Policy on Real Names

The DCO is a representation by someone stating they have the right to contribute the code they have proposed and is important for legal purposes. We have adopted the CNCF DCO Guidelines (https://github.com/cncf/foundation/blob/main/dco-guidelines.md). Which for simplicity we will include here in full:

### DCO Guidelines v1.1

The DCO is a representation by someone stating they have the right to contribute the code they have proposed for acceptance into a project: https://developercertificate.org

That representation is important for legal purposes and was the community-developed outcome after a $1 billion [lawsuit](https://en.wikipedia.org/wiki/SCO%E2%80%93Linux_disputes) by SCO against IBM. The representation is designed to prevent issues but also keep the burden on contributors low. It has proven very adaptable to other projects, is built into git itself (and now also GitHub), and is in use by thousands of projects to avoid more burdensome requirements to contribute (such as a CLA).

### DCO and Real Names

The DCO requires the use of a real name that can be used to identify someone in case there is an issue about a contribution they made.

**A real name does not require a legal name, nor a birth name, nor any name that appears on an official ID (e.g. a passport). Your real name is the name you convey to people in the community for them to use to identify you as you. The key concern is that your identification is sufficient enough to contact you if an issue were to arise in the future about your contribution.**

Your real name should not be an anonymous id or false name that misrepresents who you are.
