/* global require Buffer*/
const sha256 = require('sha256')
const bip66 = require('bip66')
const fetch = require('node-fetch')
const ec = new require('elliptic').ec('secp256k1')

const { URLSearchParams } = require('url')

// const API_HOST = 'http://razzil-api.dev.csiodev.com'
const API_HOST = 'http://localhost:3000'
const APP_KEY = '028566c1a75af63e766779fdd9556a4d48e6041edc7c012f9f727771bec0a78e74'
const APP_SECRET = '16f4e5b72fb844e0b8179126f6710c1fdee846631cff4dae0863b28e7834d878'

const ZERO = Buffer.alloc(1, 0)
function toDER(x){
  let i = 0
  while (x[i] === 0) ++i
  if (i === x.length) return ZERO
  x = x.slice(i)
  if (x[0] & 0x80) return Buffer.concat([ZERO, x], 1 + x.length)
  return x
}

const generateKeyPair = () => {
  const keyPair = ec.genKeyPair()
  return {
    privateKey: keyPair.getPrivate('hex'),
    publicKey: keyPair.getPublic(true, 'hex')
  }
}

/**
 * 
 * @param {*} message 
 * @param {*} appSecret 
 */
const sign = (message, appSecret) => {
  // const message = 'GET|/v1/payment/|1541560385699|'
  const privateKey = Buffer.from(appSecret, 'hex')
  const result = ec.sign(Buffer.from(sha256.x2(message), 'hex'), privateKey)
  let r = Buffer.from(result.r.toString(16, 64), 'hex')
  let s = Buffer.from(result.s.toString(16, 64), 'hex')
  r = toDER(r)
  s = toDER(s)
  return bip66.encode(r, s).toString('hex')
}

const request = (method, path, params, appKey, appSecret, base = API_HOST) => {
  const nonce = String(new Date().getTime())
  const sortedParams = Object.keys(params).sort().map((k) => {
    return k + '=' + encodeURIComponent(params[k])
  }).join('&')
  const content = [method, path, nonce, sortedParams].join('|')
  const headers = {
    'Biz-Api-Key': appKey,
    'Biz-Api-Nonce': nonce,
    'Biz-Api-Signature': sign(content, appSecret)
  }
  if (method == 'GET') {
    const fetchUrl = sortedParams ? base + path + '?' + sortedParams : base + path
    return fetch(fetchUrl, {
      'method': method,
      'headers': headers,
    })
  } else if (method == 'POST') {
    const urlParams = new URLSearchParams()
    for (let k in params){
      urlParams.append(k, params[k])
    }
    return fetch(base + path, {
      'method': method,
      'headers': headers,
      'body': urlParams
    })
  } else {
    throw 'unexpected method ' + method
  }
}

// const keyPair = generateKeyPair()
// console.log(keyPair);

/*
const paymentId = 'ead2a21c-ff76-4928-8652-b20e0ee51cdb'
request('GET', `/v1/payment/${paymentId}`, {}, APP_KEY, APP_SECRET)
  .then(res => {
    // console.log(res.status)
    res.json().then((data) => {
      // console.log(data)
    })
  }).catch(err => {
    console.log(err)
  })
*/

request('POST', '/v1/payment/', {
  // 'targetId': '',
  amount: 1025,
  expiry: 900
}, APP_KEY, APP_SECRET)
  .then(res => {
    // console.log(res)
    res.json().then((data)=>{
      console.log(data)
    })
  }).catch(err => {
    console.log(err)
  })
