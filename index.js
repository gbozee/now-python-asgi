const path = require('path');
const execa = require('execa');
const { readFile, writeFile } = require('fs.promised');
const getWritableDirectory = require('@now/build-utils/fs/get-writable-directory.js'); // eslint-disable-line import/no-extraneous-dependencies
const download = require('@now/build-utils/fs/download.js'); // eslint-disable-line import/no-extraneous-dependencies
const glob = require('@now/build-utils/fs/glob.js'); // eslint-disable-line import/no-extraneous-dependencies
const { createLambda } = require('@now/build-utils/lambda.js'); // eslint-disable-line import/no-extraneous-dependencies

const pip = require('./pip');
const log = require('./log');


exports.config = {
  maxLambdaSize: '5mb',
};


exports.build = async ({ files, entrypoint, config }) => {
  log.title('Starting build');

  const systemReleaseContents = await readFile(
    path.join('/etc', 'system-release'),
    'utf8',
  );
  log.info(`Build AMI verson: ${systemReleaseContents.trim()}`);

  const pythonVersion = await execa('python3', ['--version']);
  log.info(`Build python version: ${pythonVersion.stdout}`);
  log.info(`Lambda runtime: ${(config.runtime || 'python3.6 (default)')}`);

  log.heading('Downloading project');
  const srcDir = await getWritableDirectory();

  // eslint-disable-next-line no-param-reassign
  files = await download(files, srcDir);

  log.heading('Preparing python');
  const pyUserBase = await getWritableDirectory();
  process.env.PYTHONUSERBASE = pyUserBase;
  const pipPath = await pip.downloadAndInstallPip();

  log.heading('Installing project requirements');
  const requirementsTxtPath = pip.findRequirements(entrypoint, files);
  await pip.install(pipPath, srcDir, '-r', requirementsTxtPath);

  log.heading('Preparing lambda bundle');
  const originalNowHandlerPyContents = await readFile(
    path.join(__dirname, 'now_python_wsgi', 'handler.py'),
    'utf8',
  );

  log.info(`Entrypoint is ${entrypoint}`);
  const userHandlerFilePath = entrypoint
    .replace(/\//g, '.')
    .replace(/\.py$/, '');
  const nowHandlerPyContents = originalNowHandlerPyContents.replace(
    '__NOW_HANDLER_FILENAME',
    userHandlerFilePath,
  );

  const nowHandlerPyFilename = 'now__handler__python';

  await writeFile(
    path.join(srcDir, `${nowHandlerPyFilename}.py`),
    nowHandlerPyContents,
  );

  const lambda = await createLambda({
    files: await glob('**', srcDir),
    handler: `${nowHandlerPyFilename}.now_handler`,
    runtime: `${config.runtime || 'python3.6'}`,
    environment: {},
  });

  log.title('Done!');

  return {
    [entrypoint]: lambda,
  };
};
