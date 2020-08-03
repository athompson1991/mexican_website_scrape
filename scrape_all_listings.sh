scrapy crawl imparcial_oaxaca_listings
scrapy crawl informador_listings
scrapy crawl nss_oaxaca_listings
scrapy crawl oaxaca_quadratin_listings
scrapy crawl oaxaca_universal_listings
scrapy crawl rio_oaxaca_listings

python -c 'from core.utils import transfer_csvs; transfer_csvs("imparcial_oaxaca")'
python -c 'from core.utils import transfer_csvs; transfer_csvs("informador")'
python -c 'from core.utils import transfer_csvs; transfer_csvs("nss_oaxaca")'
python -c 'from core.utils import transfer_csvs; transfer_csvs("oaxaca_quadratin")'
python -c 'from core.utils import transfer_csvs; transfer_csvs("oaxaca_universal")'
python -c 'from core.utils import transfer_csvs; transfer_csvs("rio_oaxaca")'