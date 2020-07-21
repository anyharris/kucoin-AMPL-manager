# kucoin-AMPL-manager  

This app manages orders for AMPL token. Open orders need to be adjusted daily because of how AMPL's dynamic supply works.

### Installation  

Get API key, secret, and passphrase from KuCoin and put them in an `.env` file. See `example.env`.  
Copy `config.example.py` to `config.py` and adjust the `initial investment` value and the `stop_loss` and `take_profit` order parameters.  

Run `manager.py` using cron at least once per day so that it adjusts for the rebase which happens at `02:00 UTC`.  
Note that the KuCoin AMPL markets will close from about `01:40 UTC` to `02:20 UTC` and no new orders can be made during this time.
