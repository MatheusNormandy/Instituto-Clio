module.exports = {
  'Content-Security-Policy': 'default-src \'self\' https:; script-src \'self\' \'unsafe-inline\' https:; style-src \'self\' \'unsafe-inline\' https:;',
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
};