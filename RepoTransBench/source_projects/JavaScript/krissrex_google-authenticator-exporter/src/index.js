/**
 * Google Authenticator uses protobuff to encode the 2fa data.
 *
 * @param {Uint8Array} payload
 */
function decodeProtobuf(payload) {
  const protobuf = require("protobufjs");

  const root = protobuf.loadSync("./src/google_auth.proto");

  const MigrationPayload = root.lookupType("googleauth.MigrationPayload");

  const message = MigrationPayload.decode(payload);

  return MigrationPayload.toObject(message, {
    longs: String,
    enums: String,
    bytes: String,
  })
}

/**
 * Convert a base64 to base32.
 * Most Time based One Time Password (TOTP)
 * password managers use this as the "secret key" when generating a code.
 *
 * An example is: https://totp.danhersam.com/.
 *
 * @returns RFC3548 compliant base32 string
 */
function toBase32(base64String) {
  const base32 = require('./edbase32');
  const raw = Buffer.from(base64String, "base64");
  return base32.encode(raw);
}

/**
 * The data in the URI from Google Authenticator
 *  is a protobuff payload which is Base64 encoded and then URI encoded.
 * This function decodes those, and then decodes the protobuf data contained inside.
 *
 * @param {String} data the `data` query parameter from the totp migration string that google authenticator outputs.
 */
function decode(data) {
  const buffer = Buffer.from(decodeURIComponent(data), "base64");

  const payload = decodeProtobuf(buffer);

  if (payload.version != "1") {
    console.error(`Expected payload version 1, but was ${payload.version}! Please comment your payload version (which is ${payload.version}), Google Authenticator app version and how many 2FA codes you exported in https://github.com/krissrex/google-authenticator-exporter/issues/23 .`)
  }

  const accounts = payload.otpParameters.map(account => {
    account.totpSecret = toBase32(account.secret);
    return account;
  })

  return accounts;
}

/**
 * Write the json with account information to a file
 * so it can be uploaded to other password managers etc easily.
 *
 * @param {String} data A `JSON.stringify`ed list of accounts.
 */
function saveToFile(filename, data) {
  const fs = require("fs");
  if (fs.existsSync(filename)) {
    return console.error(`File "${filename}" exists!`);
  }

  fs.writeFileSync(filename, data);
}

/**
 * Generate qrcodes from the accounts that can be scanned with an authenticator app
 * @param accounts A list of the auth accounts
 */
function saveToQRCodes(accounts){

  const QRCode = require('qrcode')
  const fs = require("fs");

  const directory = "./qrCodes"
  if(!fs.existsSync(directory)){
    fs.mkdirSync(directory)
  }

  /** Windows is picky with filenames. */
  const sanitizeFilename = (filename) => filename.replace(/[\<>:"\/\\|?*#%&{}$+!`'=@]/g, "")
  
  accounts.forEach(account => {
    const name = account.name || ""
    const issuer = account.issuer || ""
    const secret = account.totpSecret

    const url = `otpauth://totp/${encodeURI(name)}?secret=${encodeURI(secret)}&issuer=${encodeURI(issuer)}`
    const file = `${directory}/${issuer || "No issuer"} (${sanitizeFilename(name)}).png`

    if(fs.existsSync(file)) {
      if (typeof file.yellow === 'function') {
        console.log(`${file.yellow()} already exists.`)
      } else {
        console.log(`${file} already exists.`)
      }
    }else{
      QRCode.toFile(file, url, (error) => {
        if(error != null){
          console.log(`Something went wrong while creating ${file}`, error)
        }
        if (typeof file.green === 'function') {
          console.log(`${file.green()} created.`)
        } else {
          console.log(`${file} created.`)
        }
      })
    }

  })
}

/**
 * Saves to json if the user said yes.
 * @param promptResult The results from the promt given to the user.
 * @param accounts A list of the auth accounts.
 */
function toJson(filename, saveToFileInput, accounts) {
  console.log(filename)
  console.log(saveToFileInput)

  if (saveToFileInput && filename) {
    console.log(`Saving to "${filename}"...`);
    saveToFile(filename, JSON.stringify(accounts, undefined, 4));
  } else {
    console.log("Not saving. Here is the data:");
    console.log(accounts);
    if (typeof "string".yellow === 'function' && typeof "'totpSecret'".blue === 'function') {
      // If chalk or color is monkeypatched
      console.log("What you want to use as secret key in other password managers is ".yellow + "'totpSecret'".blue + ", not 'secret'!".yellow);
    } else {
      console.log("What you want to use as secret key in other password managers is 'totpSecret', not 'secret'!");
    }
  }
}

module.exports = {
  decodeProtobuf,
  toBase32,
  decode,
  saveToFile,
  saveToQRCodes,
  toJson,
};