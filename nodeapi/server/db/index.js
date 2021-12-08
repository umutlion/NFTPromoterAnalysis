const mysql = require('mysql')

const pool = mysql.createPool({
    connectionLimit: 10,
    password: 'password',
    user: 'root',
    database: 'Twitter',
    host: 'localhost',
    port: '3306'
})

let tweetdb = {};

tweetdb.all = () => {
    return new Promise((resolve, reject) => {
        pool.query(`SELECT * FROM tweets4`, (err, results) => {
            if (err){
                return reject(err);
            }
            return resolve(results);
        })
    })
}

tweetdb.one = (id) => {
    return new Promise((resolve, reject)=> {
        pool.query(`SELECT * FROM tweets4 WHERE user_screen_name = ?`, [id], (err, results) => {
            if (err) {
                return reject(err);
            }
            return resolve(results[0]);
        })
    })
}



module.exports= tweetdb;