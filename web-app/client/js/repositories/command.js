/*jslint node:true, nomen: true */
"use strict";

var $ = require('jquery'),
    Promise = require('bluebird');

function Repository(server) {
    if (!(this instanceof Repository)) {
        return new Repository(server);
    }
    this._server = server.server || '';
}

Repository.prototype.getCommands = function () {
    var self = this;
    console.log(self._server)
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: self._server + '/data',
            type: 'GET',
            contentType: "text/plain",
        }).done(function (result) {
			console.log("Request completed");
            resolve(result);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            var error = new Error(errorThrown);
            error.textStatus = textStatus;
            error.jqXHR = jqXHR;
            error.errors = jqXHR.responseJSON;
            reject(error);
        });
    });
};

exports.Repository = Repository;
exports.createRepository = Repository;
