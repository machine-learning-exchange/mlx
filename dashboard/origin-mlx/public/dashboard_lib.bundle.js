!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.centraldashboard=t():e.centraldashboard=t()}(window,(function(){return function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}return n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(o,r,function(t){return e[t]}.bind(null,r));return o},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=51)}({51:function(e,t,n){"use strict";n.r(t),n.d(t,"PARENT_CONNECTED_EVENT",(function(){return o})),n.d(t,"IFRAME_CONNECTED_EVENT",(function(){return r})),n.d(t,"NAMESPACE_SELECTED_EVENT",(function(){return i})),n.d(t,"MESSAGE",(function(){return s})),n.d(t,"CentralDashboardEventHandler",(function(){return c}));const o="parent-connected",r="iframe-connected",i="namespace-selected",s="message";const c=new class{constructor(){this.window=window,this.parent=window.parent,this._messageEventListener=null,this._onParentConnected=null,this._onNamespaceSelected=null}init(e,t=!1){const n=this.window.location!==this.parent.location;e(this,n),n?(this._messageEventListener=this._onMessageReceived.bind(this),this.window.addEventListener(s,this._messageEventListener),this.parent.postMessage({type:r},this.parent.origin)):t||fetch("/api/dashboard-settings").then(e=>e.json()).then(e=>{if(e.DASHBOARD_FORCE_IFRAME){const e=this.window.location.origin+this.window.location.href.replace(this.window.location.origin,"/_");this.window.location.replace(e)}}).catch(e=>console.error(e))}detach(){this._messageEventListener&&this.window.removeEventListener(s,this._messageEventListener)}set onParentConnected(e){"function"==typeof e&&(this._onParentConnected=e)}set onNamespaceSelected(e){"function"==typeof e&&(this._onNamespaceSelected=e)}_onMessageReceived(e){const{data:t}=e;switch(t.type){case o:this._onParentConnected&&this._onParentConnected(t);break;case i:this._onNamespaceSelected&&this._onNamespaceSelected(t.value)}}}}})}));
//# sourceMappingURL=dashboard_lib.bundle.js.map