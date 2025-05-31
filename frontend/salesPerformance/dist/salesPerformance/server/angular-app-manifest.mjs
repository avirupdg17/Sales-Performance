
export default {
  bootstrap: () => import('./main.server.mjs').then(m => m.default),
  inlineCriticalCss: true,
  baseHref: '/',
  locale: undefined,
  routes: [
  {
    "renderMode": 2,
    "route": "/"
  }
],
  entryPointToBrowserMapping: undefined,
  assets: {
    'index.csr.html': {size: 23738, hash: '355fa12f8ccffd3b166fdb281388ac8c1d7cd8bd426a4a710a9947a5149a17aa', text: () => import('./assets-chunks/index_csr_html.mjs').then(m => m.default)},
    'index.server.html': {size: 17144, hash: 'b323b3f66579964a1ac428616f1500c711e9bf2a151978a85761db72c3eabc8c', text: () => import('./assets-chunks/index_server_html.mjs').then(m => m.default)},
    'index.html': {size: 105324, hash: '45dd69ebbdee8954c5b526315a920a0097b69ac1a8984eacc14302c9c03c0795', text: () => import('./assets-chunks/index_html.mjs').then(m => m.default)},
    'styles-66YXRRN4.css': {size: 7147, hash: 'hsIHghqOIgs', text: () => import('./assets-chunks/styles-66YXRRN4_css.mjs').then(m => m.default)}
  },
};
