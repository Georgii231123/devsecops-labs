# ADR-001: Repository template instead of a central runtime wrapper

## Decision

Generate normal application repositories from a versioned template rather than forcing every service through a custom runtime framework.

## Why

- generated services remain understandable without the platform tooling;
- teams can update dependencies independently;
- the platform standardizes operational concerns without coupling business logic;
- migrations can be performed as normal code changes.

## Trade-off

Template improvements are not automatically backported to every existing service. A mature implementation would pair this approach with automated upgrade pull requests.
