/* global require Buffer*/
const sha256 = require('sha256')
const bip66 = require('bip66')
const fetch = require('node-fetch')
const ec = new require('elliptic').ec('secp256k1')

const { URLSearchParams } = require('url')

// const API_HOST = 'http://razzil-api.dev.csiodev.com'
const API_HOST = 'http://razor.dev.csiodev.com'
const API_KEY = '039b4a3dd1471bf3321bb89ca42b66b4cd3b9632b47759389a7ffafd452a12e4c7'
const API_SECRET = 'e4ccd9c8c2c67fe3c07fe7d89402cf215cdf2335db16577f0b45f88123aef072'

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
    publicKey: keyPair.getPublic(true, 'hex'),
    privateKey: keyPair.getPrivate('hex')
  }
}

/**
 * 
 * @param {*} message 
 * @param {*} apiSecret 
 */
const sign = (message, apiSecret) => {
  // const message = 'GET|/v1/payment/|1541560385699|'
  const privateKey = Buffer.from(apiSecret, 'hex')
  const result = ec.sign(Buffer.from(sha256.x2(message), 'hex'), privateKey)
  let r = Buffer.from(result.r.toString(16, 64), 'hex')
  let s = Buffer.from(result.s.toString(16, 64), 'hex')
  r = toDER(r)
  s = toDER(s)
  return bip66.encode(r, s).toString('hex')
}

const request = (method, path, params = {}, apiKey = API_KEY, apiSecret = API_SECRET, base = API_HOST) => {
  const nonce = String(new Date().getTime())
  const sortedParams = Object.keys(params).sort().map((k) => {
    return k + '=' + encodeURIComponent(params[k])
  }).join('&')
  const content = [method, path, nonce, sortedParams].join('|')
  const headers = {
    'Biz-Api-Key': apiKey,
    'Biz-Api-Nonce': nonce,
    'Biz-Api-Signature': sign(content, apiSecret)
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

const keyPair = generateKeyPair()
console.log(keyPair);
/*
const paymentId = '6e7eaee9-37c1-4466-9c32-9d459c80a294'
request('GET', `/open/v1/payment/${paymentId}`)
.then(res => {
  // console.log(res.status)
  res.json().then((data) => {
    console.log(data)
  })
}).catch(err => {
  console.log(err)
})
*/
request('POST', '/open/v1/payment/', {
  // 'targetId': '',
  amount: 1025,
  expiry: 900
}, API_KEY, API_SECRET)
  .then(res => {
    // console.log(res)
    res.json().then((data)=>{
      console.log(data)
    })
  }).catch(err => {
    console.log(err)
  })

// request('GET', `/open/v1/payment`, {
//   page: 1,
//   limit: 10
// })
// .then(res => {
//   // console.log(res.status)
//   res.json().then((data) => {
//     console.log(data)
//   })
// }).catch(err => {
//   console.log(err)
// })

// request('POST', '/open/v1/payment', {
//   amount: 1024,
//   expiry: 1800
// })
// .then(res => {
//   res.json().then((data) => {
//     console.log(data)
//   })
// }).catch(err => {
//   console.log(err)
// })

// request('GET', `/open/v1/withdraw`, {
//   page: 1,
//   limit: 10
// })
// .then(res => {
//   // console.log(res.status)
//   res.json().then((data) => {
//     console.log(data)
//   })
// }).catch(err => {
//   console.log(err)
// })

// const withdrawId = 'c2532dcf-e29f-4985-a8fe-7860314f12df'
// request('GET', `/open/v1/withdraw/${withdrawId}`)
// .then(res => {
//   // console.log(res.status)
//   res.json().then((data) => {
//     console.log(data)
//   })
// }).catch(err => {
//   console.log(err)
// })

// request('POST', '/open/v1/withdraw', {
//   invoice: 'lnbc10240n1pwlqkgspp5xkxl25xd8tan0thqc0sjh57q90939aapg2uym7gkh6etgxh24wqqdqqcqzpgxqrrsszqzdlefm8d9swxhwppfhlvck6gh0cfrs6yycw576u3lsdmn8c4dsndrsh9068tujry6hs9vcjmmncz67ljk2n0ud67jnf50w0ty20kgp0dnz0d'
// })
// .then(res => {
//   res.json().then((data) => {
//     console.log(data)
//   })
// }).catch(err => {
//   console.log(err)
// })
