"use strict";
var expect = require('chai').expect;
var Query = require('../index');

function removeSpaces(textS) {
    return `${textS}`.replace(/\s+/g, '');
}

describe("graphql query builder (public cases)", function() {
    it('should accept a single find value (public)', function(){
        let expected = `product{price}`;
        let q = new Query("product").find("price");
        expect(removeSpaces(expected)).to.equal(removeSpaces(q));
    });

    it('should create a Query with function name & alias (public)', function(){
        let expected = `best : product{title}`;
        let q = new Query("product","best").find("title");
        expect(removeSpaces(expected)).to.equal(removeSpaces(q));
    });

    it('should create a Query with function name & input (public)', function(){
        let expected = `order(orderId:56789){status}`;
        let q = new Query("order",{orderId:56789}).find("status");
        expect(removeSpaces(expected)).to.equal(removeSpaces(q));
    });

    it('should create a Query with function name & input(s) (public)', function(){
        let expected = `order(orderId:56789, quantity:10){status}`;
        let q = new Query("order",{orderId:56789, quantity:10}).find("status");
        expect(removeSpaces(expected)).to.equal(removeSpaces(q));
    });

    it('should accept array as find argument (public)', function(){
        let expected = `shop{location, items}`;
        let q = new Query("shop").find(["location", "items"]);
        expect(removeSpaces(expected)).to.equal(removeSpaces(q));
    });

    it('should handle nested find (public)', function(){
        let expected = `profile{id, data{email}}`;
        let q = new Query("profile").find(["id", {data: ["email"]}]);
        expect(removeSpaces(expected)).to.equal(removeSpaces(q));
    });

    it('should stringify toString correctly (public)', function(){
        let expected = `team{members}`;
        let q = new Query("team").find("members");
        expect(removeSpaces(expected)).to.equal(removeSpaces(q.toString()));
    });

    it('should support toString with simple case (public)', function(){
        let expected = `item{name}`;
        let q = new Query("item").find("name");
        expect(removeSpaces(expected)).to.equal(removeSpaces(q.toString()));
    });
});