/*
The code below was build
as requested by AI center for
testing purpose
Author: Islam Nader Awad
*/

//Endpoint URL
var url = 'http://localhost:5000/api/List'


function onRefresh() {
    //http get request
    fetch(url)
    .then(res => res.json())
    .then((data) => {
        var info = data['data'][0];
        //get scanned data
        mapData(info);
    })
    .catch(err => { throw err });
} 

//Function to map data into table
function mapData(info) {
    console.log(info)
    var email = '', phone = ''
    for (let i in info) {
        email = info[i]['email']
        phone = info[i]['phone']
        let tableRef = document.getElementById('list');
        let row = tableRef.insertRow(1,1);
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        cell1.innerHTML = email;
        cell2.innerHTML = phone;    
    }
}