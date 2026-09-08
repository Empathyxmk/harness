/**
  Chapter 1 public tests with different data
  Author: Public test generator
*/

"use strict";

const R = require('ramda');
const _ = require('lodash');

describe('Chapter 1 - Public Data', function () {

	// Use "run" as an alias in chapter 1. This is shown to just
	// warm up to the concept of composition
	const run = R.compose;

	test("Listing 1.1 Functional printMessage with new data", function () {
		const printToConsole = str => {
			console.log(str);
			return str;
		};
		const toUpperCase = str => str.toUpperCase();
		const echo = R.identity;

		const printMessage = run(printToConsole, toUpperCase, echo);
		expect(printMessage('functional')).toEqual('FUNCTIONAL');
	});

	test("Listing 1.2 Extending printMessage with new data", function () {
		const printToConsole = str => {
			console.log(str);
			return str;
		};
		const toUpperCase = str => str.toUpperCase();
		const echo = R.identity;

		const repeat = (times) => {
			return function (str = '') {
				let tokens = [];
				for (let i = 0; i < times; i++) {
					tokens.push(str);
				}
				return tokens.join(' ');
			};
		};

		const printMessage = run(printToConsole, repeat(2), toUpperCase, echo);
		expect(printMessage('public test')).toEqual('PUBLIC TEST PUBLIC TEST');
	});

	test("Listing 1.3 Imperative showStudent function with side effects (public test)", function () {
		// Use a different student and update helper db for this test
		const db = {
			find: ssn => {
				if (ssn === '222-33-4444') {
					return { ssn: '222-33-4444', firstname: 'Ada', lastname: 'Lovelace' };
				}
				return null;
			}
		};

		function showStudent(ssn) {
			let student = db.find(ssn);
			if (student !== null) {
				let studentInfo = `<p>${student.ssn},${student.firstname},${student.lastname}</p>`;
				console.log(studentInfo);
				return studentInfo;
			}
			else {
				throw new Error('Student not');
			}
		}

		expect(showStudent('222-33-4444')).toEqual('<p>222-33-4444,Ada,Lovelace</p>');
	});

	const curry = R.curry;

	test("Listing 1.4 Decomposing the showStudent program (public test)", function () {
		const db = {
			find: ssn => {
				if (ssn === '333-22-1111') {
					return { ssn: '333-22-1111', firstname: 'Grace', lastname: 'Hopper' };
				}
				return null;
			}
		};

		const find = curry((db, id) => {
			let obj = db.find(id);
			if (obj === null) {
				throw new Error('Object not found!');
			}
			return obj;
		});

		const csv = student => `${student.ssn}, ${student.firstname}, ${student.lastname}`;

		const append = curry((source, info) => {
			source(info);
			return info;
		});

		const showStudent = run(
			append(console.log),
			csv,
			find(db)
		);

		expect(showStudent('333-22-1111')).toEqual('333-22-1111, Grace, Hopper');
	});

	test("Listing 1.5 Programming with function chains (public test)", function () {
		const enrollments = [
			{
				enrolled: 2,
				grade: 75
			},
			{
				enrolled: 1,
				grade: 65
			},
			{
				enrolled: 3,
				grade: 85
			}
		];

		const result =
			_.chain(enrollments)
				.filter(student => student.enrolled > 1)
				.map(_.property('grade'))
				.mean()
				.value();

		console.log(result);

		expect(result).toEqual(80);
	});
});