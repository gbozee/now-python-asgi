const path = require('path');
const fetch = require('node-fetch');
const execa = require('execa');
const { createWriteStream } = require('fs');
const getWritableDirectory = require('@now/build-utils/fs/get-writable-directory.js'); // eslint-disable-line import/no-extraneous-dependencies

const log = require('./log');

const url = 'https://bootstrap.pypa.io/get-pip.py';


async function install(pipPath, srcDir, ...args) {
  log.subheading('Installing python packages');
  log.info(`Running "pip install -t ${srcDir} ${args.join(' ')}"`);
  try {
    const ret = await execa(pipPath, ['install', '-t', srcDir, ...args]);
    log.info(ret.stdout);
  } catch (err) {
    log.error(`Failed to run "pip install -t ${srcDir} ${args.join(' ')}"`);
    throw err;
  }
}


async function downloadGetPipScript() {
  const res = await fetch(url);

  if (!res.ok || res.status !== 200) {
    throw new Error(`Could not download "get-pip.py" from "${url}"`);
  }

  const dir = await getWritableDirectory();
  const filePath = path.join(dir, 'get-pip.py');
  const writeStream = createWriteStream(filePath);

  return new Promise((resolve, reject) => {
    res.body
      .on('error', reject)
      .pipe(writeStream)
      .on('finish', () => resolve(filePath));
  });
}


async function downloadAndInstallPip() {
  log.subheading('Installing pip');

  if (!process.env.PYTHONUSERBASE) {
    throw new Error(
      'Could not install "pip": "PYTHONUSERBASE" env var is not set',
    );
  }
  const getPipFilePath = await downloadGetPipScript();

  log.info('Running "python get-pip.py"');
  try {
    const ret = await execa('python3', [getPipFilePath, '--user']);
    log.info(ret.stdout);
  } catch (err) {
    log.error('Could not install pip');
    throw err;
  }
  return path.join(process.env.PYTHONUSERBASE, 'bin', 'pip');
}


function findRequirements(entrypoint, files) {
  log.subheading('Searching for "requirements.txt"');

  const entryDirectory = path.dirname(entrypoint);
  const requirementsTxt = path.join(entryDirectory, 'requirements.txt');

  if (files[requirementsTxt]) {
    log.info('Found local "requirements.txt"');
    return files[requirementsTxt].fsPath;
  }

  if (files['requirements.txt']) {
    log.info('Found global "requirements.txt"');
    return files['requirements.txt'].fsPath;
  }

  log.info('No "requirements.txt" found, using builder requirements');
  return path.join(__dirname, 'requirements.txt');
}


module.exports = {
  install, downloadAndInstallPip, findRequirements,
};
