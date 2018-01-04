/*jslint node:true */
"use strict";

var ko = require('knockout'),
    components = require('./components'),
    createRepositories = require('./repositories').createRepositories;

components.register();
var repositories = createRepositories({"server" : "http://127.0.0.1:8080"});

function App() {
    this.routes = {
        '/': 'list'
    };
    this.repositories = repositories;
}

ko.applyBindings(new App());
