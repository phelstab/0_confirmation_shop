from cryptos import *
c = Bitcoin(testnet=True)
priv = sha256('a big long brainwallet password')
priv
pub = c.privtopub(priv)
pub
addr = c.pubtoaddr(pub)
addr
inputs = c.unspent(addr)
inputs