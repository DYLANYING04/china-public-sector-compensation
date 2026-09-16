# Contributing Cases

Thank you for helping expand the public-source coverage. A useful contribution is a reproducible case, a portal pattern, or a correction to a cited number.

## Before You Submit

1. Search the repository's [case studies](cases/README.md) and [benchmark corpus](benchmark/README.md) to avoid duplicates.
2. Use only public material. Do not submit internal documents, personal salary slips, personal data, login-protected content, or content that identifies ordinary employees.
3. Keep `报表事实` separate from `专家判断`. A conclusion about a special award must be labelled as expert judgment, with its basis and confidence.

## A Reproducible Case Needs

- exact official unit name, region, and report year;
- official landing-page URL and attachment URL when different;
- publisher, publication date, page/table/row location, and original amount unit;
- the entity, funding, and personnel scope for every numerator and denominator;
- the calculation expression and the resulting evidence state;
- a short search log, including rejected sources and any access barrier.

Use the `New institution request`, `Data correction`, or `Portal pattern` issue forms. A maintainer will not publish an amount as a fact until the raw public source is independently checked.

## Pull Requests

- Keep a pull request limited to one case, portal pattern, or documentation change.
- Add or extend a focused test when calculator behavior changes.
- Run `python -m unittest discover -s tests -v` before opening the pull request.
- Do not add downloaded government reports to the repository unless the file is essential for a test and redistribution is clearly permitted; cite the official URL instead.

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
