# Contributing to Discovery

The team at Discovery welcomes contributions from the community. There are many ways to get involved!

Thanks for taking the time to contribute! ❤️

> And if you like the project but don't have time to contribute, that's perfectly okay. There are other simple ways to support the project and show your appreciation, which we would greatly appreciate:
> - Star the project
> - Tweet about it
> - Contribute to our [Docs](https://github.com/0bytes-security/discovery-ce/tree/docs)
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

## Code of Conduct

This project and everyone participating in it is governed by the
[Code of Conduct](https://github.com/0bytes-security/discovery-ce/blob/main/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to [info@0bytes.io](mailto:info@0bytes.io).

## Provide Feedback

You might find things that can be improved while you are using Discovery. You can help by [submitting an issue](https://github.com/0bytes-security/discovery-ce/issues/new) when:

* **Bugs:** If Discovery crashes, encounters errors, or behaves unexpectedly. Please provide details about the issue, steps to reproduce it, your environment, and any relevant logs or error messages.
* **Feature Requests:** If a new feature or an improvement to existing functionality would enhance the utility or usability of Discovery.  Describe the desired feature and how it would benefit users.
* **Documentation Improvements:**  If you find the documentation unclear, incomplete, or outdated, please submit an issue suggesting improvements. 

Before creating a new issue, please confirm that an existing issue doesn't already exist.

We will then take care of the issue as soon as possible.

## Contributing Code

We encourage you to reach out to us on [GitHub Discussions](https://github.com/0bytes-security/discovery-ce/discussions/) before starting work on significant contributions, especially core features. This helps ensure alignment with the project's roadmap, get valuable feedback early on, and avoids potential duplication of effort.  

**Here are some guidelines for posting on GitHub Discussions before making a big code contribution:**

* **Title:** Give your discussion a clear and descriptive title (e.g., "Feature Proposal: Integrate [Tool Name] as a Task").
* **Description:** 
    - Explain the problem you're trying to solve or the feature you'd like to add. 
    - Provide context and explain your proposed solution. 
    - If possible, include mockups, diagrams, or code examples.
    - Ask specific questions for feedback.

### Steps to Contribute Code

Follow the following steps to ensure your contribution goes smoothly.

1. Read and follow the steps outlined in the [Discovery Contributing Policy](README.md#contributing).
1. [Fork](https://help.github.com/articles/working-with-forks/) the GitHub Repository allowing you to make the changes in your own copy of the repository.
1. Create a [GitHub issue](https://github.com/0bytes-security/discovery-ce/issues) if one doesn't exist already.
1. [Prepare your changes](/PREPARING_YOUR_CHANGES.md) and ensure your commits are descriptive. The document contains an optional commit template, if desired.
1. Ensure that you sign off on all your commits to comply with the DCO v1.1. We have more details in [Prepare your changes](/PREPARING_YOUR_CHANGES.md).
1. Ensure that you have no lint errors. We use `ruff` as our linter, You can check for linting errors by running `nx run api:lint` in the root of the project.
1. Create a pull request on GitHub. If you're new to GitHub, read about [pull requests](https://help.github.com/articles/about-pull-requests/). You are welcome to submit your pull request for commentary or review before it is complete by creating a [draft pull request](https://help.github.com/en/articles/about-pull-requests#draft-pull-requests). Please include specific questions or items you'd like feedback on.
1. A member of the Discovery team will review your PR within three business days (excluding any holidays) and either merge, comment, and/or assign someone for review.
1. Work with the reviewer to complete a code review. For each change, create a new commit and push it to make changes to your pull request. When necessary, the reviewer can trigger CI to run tests prior to merging.
1. Once you believe your pull request is ready to be reviewed, ensure the pull request is no longer a draft by [marking it ready for review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request).
1. The reviewer will look over your contribution and either approve it or provide comments letting you know if there is anything left to do. We try to give you the opportunity to make the required changes yourself, but in some cases, we may perform the changes ourselves if it makes sense to (minor changes or for urgent issues). We do our best to review PRs promptly, but complex changes could require more time.
1. After completing your review, a Discovery team member will trigger merge to run all tests. Upon passing, your change will be merged into `main`, and your pull requests will be closed. All merges to `main` create a new release, and all final changes are attributed to you.

#### What Does Contributing Mean for You?

Here is what being a contributor means for you:

* License all our contributions to the project under the Apache License, Version 2.0
* Have the legal rights to license our contributions ourselves, or get permission to license them from our employers, clients, or others who may have them

