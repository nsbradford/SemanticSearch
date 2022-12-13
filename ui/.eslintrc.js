module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    // jest: true, // https://stackoverflow.com/questions/56398742/eslint-throws-no-undef-errors-when-linting-jest-test-files
  },
  extends: [
    'next/babel',
    'next/core-web-vitals',
    // these were leftover from other project
    // 'plugin:react/recommended',
    // 'airbnb',
    'plugin:import/errors',
    'plugin:import/warnings',
    'plugin:import/typescript',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['react', '@typescript-eslint'],
  extends: 'next/core-web-vitals',
  rules: {
    // https://typescript-eslint.io/rules/no-useless-constructor/
    'no-useless-constructor': 'off',
    '@typescript-eslint/no-useless-constructor': ['error'],

    // https://stackoverflow.com/questions/67411154/eslint-no-unused-vars-on-function-parameters-within-typescript-types-interfa
    // http://eslint.org/docs/rules/no-unused-vars#argsignorepattern
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],

    // https://stackoverflow.com/questions/55614983/jsx-not-allowed-in-files-with-extension-tsxeslintreact-jsx-filename-extensio
    'react/jsx-filename-extension': [1, { extensions: ['.tsx', '.ts'] }],

    // https://github.com/prettier/prettier/issues/6456
    'react/jsx-one-expression-per-line': 'off',
  },
};
