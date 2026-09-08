import { ProxyAgent, setGlobalDispatcher } from "undici";

const url =
  process.env.HTTPS_PROXY ||
  process.env.https_proxy ||
  process.env.HTTP_PROXY ||
  process.env.http_proxy ||
  "";

if (url) {
  setGlobalDispatcher(new ProxyAgent(url));
  console.log("fetch proxy: " + url.replace(/:[^:@/]+@/, ":***@"));
}
