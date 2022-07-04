
// NH-DL

// modify this value if you cant
// get past the CLOUDFLARE challenge in time
// keep in mind this is in milliseconds
const CLOUDFLARE_WAIT = 15000;

const fs = require("fs");
const puppeteer = require("puppeteer-extra");
const NothingAtAllWhatsoever = require("puppeteer-extra-plugin-stealth");
const { INTER_RES_PRIOR } = require("puppeteer");
const NothingAtAllISwear = require("puppeteer-extra-plugin-adblocker");

puppeteer.use(NothingAtAllWhatsoever());
puppeteer.use(NothingAtAllISwear({
  interceptResolutionPriority: INTER_RES_PRIOR,
  blockTrackers: true
}));
puppeteer.use(
  require("puppeteer-extra-plugin-minmax")()
);
puppeteer.use(
  require("puppeteer-extra-plugin-anonymize-ua")({
    stripHeadless: true,
    makeWindows: true,
    customFn: null
  })
);

//console.log(process.argv)

console.log("I know this looks sketchy as all hell, but\nDon't mind me. \nUnfortunately to break CloudFlare a new process has to be spun up.\nSo sit back and let this do it's thing\n~ star (0xSTAR) <3 | https://github.com/0xSTAR/NH-DL");

const PROPER_LNK = process.argv[2];

//console.log(PROPER_LNK)

//console.log(process.argv);

const _TIMEOUT_MS_ = CLOUDFLARE_WAIT;

// custom sleepy function
sleepy_sleep = function(x) {
    const SLEEPY_CONST = x; // keep in mind that X is for milliseconds

    const start = new Date().getTime();
    var end;
    do {
    	end = new Date().getTime();
    } while ( (end - start) < SLEEPY_CONST );
};

const SLICE_CONST_ST = 0x1b92;
const SLICE_CONST_ED = -0x14;

(async() => {

    const IS_HEADLESS = false;

    const browser = await puppeteer.launch({headless: IS_HEADLESS});
    //const page2 = await browser.newPage();
    //page2.setViewport({width:1280, height:720});
    //page2.goto("https://github.com/0xSTAR/NH-DL");


    const page = await browser.newPage();
    //page.setViewport({width:1280, height: 720});
    await page.goto(PROPER_LNK);
    page.minimize();


    //sleepy_sleep();
    await page.waitForTimeout(_TIMEOUT_MS_);

    const PAGE_HTML_AND_JSON = await page.content();

    fs.writeFile("BREAK_IT.json",/*__COOKIE_BUFF*/ PAGE_HTML_AND_JSON.slice(
      SLICE_CONST_ST, SLICE_CONST_ED), (err_on_callback) => {
        if (err_on_callback) throw err_on_callback;
        console.log("SUCCESS!!");
    }

    );

    await browser.close();

})
();
