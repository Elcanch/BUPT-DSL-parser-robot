/*
 * @Author: Elichen 2954855725@qq.com
 * @Date: 2024-12-17 18:28:55
 * @LastEditors: Elichen 2954855725@qq.com
 * @LastEditTime: 2024-12-17 18:59:36
 * @FilePath: \code\py\MyDsl\dsl-app\jest.config.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
module.exports = {
    moduleFileExtensions: ['js', 'json', 'vue'],
    transform: {
      '.*\\.(vue)$': 'vue-jest',
      '^.+\\.js$': 'babel-jest',
    },
    collectCoverage: true,
    collectCoverageFrom: [
      '<rootDir>/src/**/*.{js,vue}',
      '!<rootDir>/src/main.js',
      '!<rootDir>/src/router.js',
      '!<rootDir>/src/store.js'
    ],
    coverageDirectory: '<rootDir>/test/coverage',
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1',
      'monaco-editor': '<rootDir>/tests/__mocks__/monaco-editor.js'
    },
    snapshotSerializers: [
      'jest-serializer-vue'
    ],
    testMatch: [
      '**/tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx)'
    ],
    testURL: 'http://localhost/'
  };