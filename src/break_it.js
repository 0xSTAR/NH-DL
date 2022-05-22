const fs = require("fs")
const puppeteer = require("puppeteer-extra");
const NothingAtAllWhatsoever = require("puppeteer-extra-plugin-stealth");

puppeteer.use(NothingAtAllWhatsoever());
//let filehandle;

//console.log(process.argv)

console.log("I know this looks sketchy as all hell, but\nDon't mind me. \nUnfortunately to break CloudFlare a new process has to be spun up.\nSo sit back and let this do it's thing\n~ star (0xSTAR) <3 | https://github.com/0xSTAR/NH-DL")

const PROPER_LNK = process.argv[2];

//console.log(PROPER_LNK)
//console.log("HI!")

//console.log(process.argv);

const _TIMEOUT_MS_ = 11000; 

// custom sleepy function
sleepy_sleep = function() {
    const start = new Date().getTime();
    while (true)
    {
        var end = new Date().getTime();
        if ( (end - start) >= 20000)
        {
            break;
        } 
    }
};

(async() => {

    /* const screen = {
        width: 720,
        height: 1080,
        deviceScaleFactor: 1,
        isMobile: true,
        hasTouch: true,
        isLandScape: true
    };

    const MS_SLOWDOWN = 500;

    const browser = await puppeteer.launch(
        {
            headless: false,
            defaultViewport: screen,
            slowMo: MS_SLOWDOWN,
            dumpio: true,
            devtools: false,
            waitForInitialPage: true,
            product: "chrome"
        }*/
    //)//, executablePath: "C:/Program Files (x86)/Microsoft/Edge/Application/msedge"});

    const IS_HEADLESS = true;

    const browser = await puppeteer.launch({headless: IS_HEADLESS});
    const page2 = await browser.newPage();
    page2.goto("https://github.com/0xSTAR/NH-DL");
    //const page3 = await browser.newPage();
    //page3.goto("https://www.reddit.com/r/animepiracy/comments/uu7hwm/nhdl_v110_bye_cloudflare/");

    //console.log(await browser.userAgent());

    const page = await browser.newPage();
    //const JSON_RESPONSE = await page.goto(PROPER_LNK);
    await page.goto(PROPER_LNK);
    //await page.screenshot({ path: "example.png", fullPage: true});
    
    //sleepy_sleep();
    await page.waitForTimeout(_TIMEOUT_MS_);

    //const TRUE_JSON = await JSON_RESPONSE.json();
    //console.log(TRUE_JSON);
    const PAGE_HTML_AND_JSON = await page.content();

    //await page.screenshot({ path: "example2.png"})
    //console.log(await page.cookies());

    const __COOKIES = await page.cookies();
    //try
    //{
        //filehandle = await open("break_cookies.txt","w");
        //filehandle.write(stringify(__COOKIES));
    //}
    //finally {
        //await filehandle?.close();
    //}
    var __COOKIE_BUFF = "";
    __COOKIE_BUFF = JSON.stringify(__COOKIES,null,2)
    
    fs.writeFile("BREAK_IT.json",/*__COOKIE_BUFF*/ PAGE_HTML_AND_JSON.slice(131, -20), (err_on_callback) => {
        if (err_on_callback) throw err_on_callback;
        console.log("SUCCESS!!")
    }
    
    );

    await browser.close();

})
();