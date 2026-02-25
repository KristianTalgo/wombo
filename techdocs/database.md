Migrasjoner ligger i /migrations.

Ved oppstart av web-applikasjonen kjøres migrate.py som:
1. sjekker schema_migrations
2. kjører nye SQL-filer
3. markerer dem som applied
