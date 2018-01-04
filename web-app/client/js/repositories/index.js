/*jslint node:true */
"use strict";

exports.createRepositories = function (options) {
    return {
        command: require('./command').createRepository(options)
    };
};
