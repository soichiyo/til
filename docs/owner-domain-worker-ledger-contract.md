# Public Owner / Domain / Worker Ledger Contract

## Scope and public boundary

This is a public-safe contract for the TIL repository.

```yaml
owner: personal/soichiyo
scope: project/soichiyo/til
visibility: public-safe-contract
private_owner_ledger: pull-by-reference
distribution: default-deny
domains: []
workers: []
```

The private owner ledger is not stored, copied, synchronized, or reconstructed
in this repository. This public contract may point to that private boundary by
reference only. Domain and Worker entries remain empty until a separately
authorized, public-safe entry is accepted.

## Lifecycle contract

- **Creation:** propose a public-safe Domain or Worker entry against the scope
  above. Creation does not enable distribution or alter any consumer path.
- **Return:** a Worker returns only its public-safe result to its owning Domain
  by reference; it does not copy private owner-ledger material here.
- **Acceptance:** the owning Domain records acceptance only after the returned
  result is checked against this contract. Until then, the entry is not closed.
- **Closure:** close an accepted entry with its public-safe outcome and a
  reference to the owning Domain record. Do not add task history to this repo.
- **Retention:** retain only public-safe contract entries and references. The
  private owner ledger follows its own private retention policy.
- **Onboarding:** new participants read this contract, use the declared owner
  and scope, and treat distribution as denied unless separately authorized.
- **Offboarding:** remove access at the private owner-ledger boundary and
  return any private material there; this repository retains no private copy.
- **Archive or disable rollback:** archive a public-safe entry or disable its
  reference without moving, deleting, switching, or retiring a checkout,
  branch, consumer, or active/default path.

## Distribution rule

Distribution is default-deny. A consumer is eligible only through a separate,
explicit authorization; this contract performs no sync or distribution itself.
The active/default consumer path remains outside the scope of this document.
