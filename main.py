import os, sys, io
import M5
from M5 import *
import network
import time
import requests2



eth_label = None
btc_label = None
image0 = None
image1 = None
time_label = None
line0 = None
error_msg_label = None
wlan = None
http_req = None


screen_dirc = None
btc_price = None
gryo_y = None
gryo_x = None
eth_price = None
gryo_z = None
prices = None
previous_btc_price = None
previous_eth_price = None

# Describe this function...
def update_time():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  time_label.setText(str((str(((str(((time.localtime())[0])) + str('/')))) + str(((str(((str(((time.localtime())[1])) + str('/')))) + str(((str(((time.localtime())[2])) + str(((str(' ') + str(((str(((time.localtime())[3])) + str(((str(':') + str(((time.localtime())[4]))))))))))))))))))))

# Describe this function...
def check_wifi():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  if (wlan.status()) == (network.STAT_HANDSHAKE_TIMEOUT):
    clear_screen()
    error_msg_label.setVisible(True)
    error_msg_label.setText(str('err-handshake'))
    print('err-handshake')
    wifi_reconnect()
  elif (wlan.status()) == (network.STAT_NO_AP_FOUND):
    clear_screen()
    error_msg_label.setVisible(True)
    error_msg_label.setText(str('err-NO_AP'))
    print('err-NO_AP')
    wifi_reconnect()
  elif (wlan.status()) == (network.STAT_WRONG_PASSWORD):
    clear_screen()
    error_msg_label.setVisible(True)
    error_msg_label.setText(str('err-WRONG_PASSWORD'))
    print('err-WRONG_PASSWORD')
    wifi_reconnect()
  elif (wlan.status()) == (network.STAT_BEACON_TIMEOUT):
    clear_screen()
    error_msg_label.setVisible(True)
    error_msg_label.setText(str('err-BEACON_TO'))
    print('err-BEACON_TO')
    wifi_reconnect()
  elif (wlan.status()) == (network.STAT_ASSOC_FAIL):
    clear_screen()
    error_msg_label.setVisible(True)
    error_msg_label.setText(str('err-ASSOC_F'))
    print('err-ASSOC_F')
    wifi_reconnect()
  elif (wlan.status()) == (network.STAT_IDLE):
    clear_screen()
    print('IDLE')
    wifi_reconnect()
  elif (wlan.status()) == (network.STAT_CONNECTING):
    print('connecting')
  elif (wlan.status()) == (network.STAT_GOT_IP):
    pass
  else:
    error_msg_label.setVisible(True)
    error_msg_label.setText(str('unknown error'))
    print('face_unknown_wifi_reason')

# Describe this function...
def wifi_reconnect():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  try:
    print('try_wifi_reconnect')
    wlan.disconnect()
    wlan.connect('猜對就讓你連蠢蛋', 'oylt0925')
    print('wifi_reconnecting....')
    time.sleep(3)
  except:
    print('wifi_reconnect_fail')
    check_wifi()


# Describe this function...
def show_screen():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  eth_label.setVisible(True)
  btc_label.setVisible(True)
  image0.setVisible(True)
  image1.setVisible(True)
  line0.setVisible(True)
  error_msg_label.setVisible(False)
  time_label.setVisible(True)

# Describe this function...
def clear_screen():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  eth_label.setVisible(False)
  btc_label.setVisible(False)
  image0.setVisible(False)
  image1.setVisible(False)
  line0.setVisible(False)
  error_msg_label.setVisible(False)
  time_label.setVisible(False)

# Describe this function...
def check_dirc():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  if screen_dirc != 1 and gryo_y >= 0.8:
    clear_screen()
    screen_dirc = 1
    Widgets.setRotation(0)
    print('turn 1')
    show_screen()
  elif screen_dirc != 2 and gryo_x >= 0.8:
    clear_screen()
    screen_dirc = 2
    Widgets.setRotation(1)
    print('turn 2')
    show_screen()
  elif screen_dirc != 3 and gryo_y <= -0.8:
    clear_screen()
    screen_dirc = 3
    Widgets.setRotation(2)
    print('turn 3')
    show_screen()
  elif screen_dirc != 4 and gryo_x <= -0.8:
    clear_screen()
    screen_dirc = 4
    Widgets.setRotation(3)
    print('turn 4')
    show_screen()

# Describe this function...
def getprice():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  print('get_price......')
  try:
    http_req = requests2.get((str('https://min-api.cryptocompare.com/data/pricemulti?fsyms=') + str(((str('BTC,ETH') + str('&tsyms=USD'))))), headers={'Content-Type': 'application/json'})
    print('get_price_done')
    prices = http_req.json()
    print(str(prices))
  except:
    print('get_price fail touch function')

  try:
    http_req.close()
  except:
    print('http close fail touch function')


# Describe this function...
def price_update():
  global screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price, eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req
  try:
    getprice()
    btc_price = int((prices['BTC'])['USD'])
    eth_price = int((prices['ETH'])['USD'])
    btc_label.setText(str(btc_price))
    eth_label.setText(str(eth_price))
    if btc_price > previous_btc_price:
      eth_label.setColor(0x33cc00, 0x141414)
    else:
      eth_label.setColor(0xcc0000, 0x0f0f0f)
    if eth_price > previous_eth_price:
      eth_label.setColor(0x33cc00, 0x141414)
    else:
      eth_label.setColor(0xcc0000, 0x0f0f0f)
    previous_btc_price = btc_price
    previous_eth_price = eth_price
  except:
    check_wifi()



def setup():
  global eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req, screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price

  M5.begin()
  eth_label = Widgets.Label("load...", 42, 82, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
  btc_label = Widgets.Label("load...", 42, 29, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
  image0 = Widgets.Image("res/img/ethereum (1).png", 6, 80, scale_x=1, scale_y=1)
  image1 = Widgets.Image("res/img/bitcoin (2).png", 8, 26, scale_x=1, scale_y=1)
  time_label = Widgets.Label("load...", 9, 6, 1.0, 0x00ff0d, 0x222222, Widgets.FONTS.DejaVu9)
  line0 = Widgets.Line(12, 69, 120, 69, 0xffffff)
  error_msg_label = Widgets.Label("err", 37, 70, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu9)

  wlan = network.WLAN(network.STA_IF)
  wlan.config(reconnects=3)
  wlan.active(True)
  wlan.config(dhcp_hostname='brianoy_atoms3')
  wlan.connect('猜對就讓你連蠢蛋', 'oylt0925')
  previous_btc_price = 0
  previous_eth_price = 0
  btc_price = 0
  eth_price = 0
  error_msg_label.setVisible(False)
  time.timezone('GMT-8')


def loop():
  global eth_label, btc_label, image0, image1, time_label, line0, error_msg_label, wlan, http_req, screen_dirc, btc_price, gryo_y, gryo_x, eth_price, gryo_z, prices, previous_btc_price, previous_eth_price
  M5.update()
  time.sleep(3)
  (gryo_x, gryo_y, gryo_z) = Imu.getAccel()
  print('price_upd')
  price_update()
  print('chk_wifi')
  check_wifi()
  print('upd_time')
  update_time()
  print('chk_dirction')
  check_dirc()


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
