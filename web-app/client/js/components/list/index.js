/*jslint node:true */
"use strict";

var ko = require('knockout');

ko.observableArray.fn.pushAll = function(valuesToPush) {
      var underlyingArray = this();
      this.valueWillMutate();
      ko.utils.arrayPushAll(underlyingArray, valuesToPush);
      this.valueHasMutated();
      return this;  //optional
  };

function ViewModel(ctx) {
    var self = this;

    self.commands = ko.observableArray()

    ctx.repositories.command.getCommands(
    ).then(function(result){
      self.commands.pushAll(result.results)
    }).catch(function(e){
      console.log(e)
    })

    self.showRecord = function(obj){
        var position = obj.position;
        position = position - 90;
        var c=document.getElementById("canvas");
        var canvas = c.getContext("2d");
        var width = c.width
        var height = c.height
        var originX = width/2
        var originY = height/2
        console.log("position: "+position);
        console.log("from x: "+originX);
        console.log("from y:"+originY);
        var r = 200
        canvas.clearRect(0, 0, width, height);
        canvas.beginPath();
        canvas.moveTo(originX , originY);
        var toX = originX + r * Math.cos(Math.PI * position /180)
        var toY = originY + r * Math.sin(Math.PI * position /180)
        if (toX == originX){
          console.log("position 0 - 180");
          canvas.lineTo(toX - 20 , toY)
          canvas.lineTo(toX + 20, toY)
        } else if (toY == originY){
          console.log("Position 90 - 270");
          canvas.lineTo(toX, toY +10)
          canvas.lineTo(toX, toY - 10)
        } else if (toX < originX && toY > originY || toX > originX && toY < originY){
          console.log("Position x< y> or x> y<");
          canvas.lineTo(toX - 20, toY - 10)
          canvas.lineTo(toX + 20, toY + 10)
        } else {
          console.log("Position x< y< or x> y>");
          canvas.lineTo(toX + 20, toY - 10)
          canvas.lineTo(toX - 20, toY + 10)
        }
        console.log("to x: "+(originX + r * Math.cos(Math.PI * position /180)));
        console.log("to y: "+(originY + r * Math.sin(Math.PI * position /180)));
        canvas.fillStyle = "#FF000099"
        canvas.fill()
    };

    self.firstName = ko.observable('First');
    self.lastName = ko.observable('Last');
    self.users = ko.observableArray();
    self.add = function () {
        self.users.push({
            first: self.firstName(),
            last: self.lastName(),
        });
    };
    self.remove = function () {
        // this is the user not the VM
        self.users.splice(self.users.indexOf(this), 1);
    };
}

exports.register = function () {
    ko.components.register('list', {
        template: require('./template.html'),
        viewModel: ViewModel
    });
};
