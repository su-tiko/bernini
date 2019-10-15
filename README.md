# Zapatos Bernini
Simple Django application for managing orders in an online store.
It just uses Django Admin modified for being usable by non-staff users.

## Setup
`pip install -r requirements.txt`

There is included an example database so there is no need of migrating it.

### Accounts
There are 3 accounts:

| User | Password |
| ---- | -------- |
| admin | passwordpassword |
| client | passwordpassword |
| client2 | passwordpassword |

Each client can just see their orders while admin can see all.


## Notes
As it is a demo app there are many things that are not good for a production environment:

- We should get some config from environment to follow factor12.
- Email backend is set to Console.
- Missing unit tests.