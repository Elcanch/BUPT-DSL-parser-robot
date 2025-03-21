const MonacoEditorPlugin = require("monaco-editor-webpack-plugin");

module.exports = {
    lintOnSave: false,
    configureWebpack: {
        plugins: [
            new MonacoEditorPlugin({
                languages: ["javascipt", "css", "html", "typescript"],
            }),
        ],
    },
    productionSourceMap: false,
};