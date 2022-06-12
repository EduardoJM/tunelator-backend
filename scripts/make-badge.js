const { existsSync, readFileSync, writeFileSync } = require('fs');
const { exit } = require('process');
const { get } = require('https');

if (!existsSync('./tunelator/coverage.json')) {
    exit(0);
}

const file = readFileSync('./tunelator/coverage.json');
const content = file.toString('utf-8');
const json = JSON.parse(content);

const { totals } = json;
const { percent_covered_display } = totals;

const getColour = (coverage) => {
    if (coverage < 80) {
        return 'red';
    }
    if (coverage < 90) {
        return 'yellow';
    }
    return 'brightgreen';
};

const getBadge = (coverage) => {
    const colour = getColour(parseInt(coverage, 10));
  
    return `https://img.shields.io/badge/Coverage${encodeURI(': ')}${coverage}${encodeURI('%')}-${colour}.svg`;
}

const download = (url, cb) => {
    get(url, (res) => {
        let file = '';
        res.on('data', (chunk) => {
            file += chunk;
        });
        res.on('end', () => cb(null, file));
    }).on('error', err => cb(err));
}

download(getBadge(percent_covered_display), (_, res) => {
    writeFileSync('./.github/badges/coverage.svg', res);
});

