/*jshint esversion: 8 */
const { MongoClient } = require('mongodb');
const fs = require('fs');

const url = process.env.MONGO_URL || 'mongodb://localhost:27017';
const dbName = 'dealershipsDB';
