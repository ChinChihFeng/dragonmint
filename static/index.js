function scan_miner(name) {
    var request = new XMLHttpRequest();
    var params = 'network=192.1.3.0/24';
    request.open('POST', `/${name}`);
    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    request.onload = () => {
        const response = request.responseText;
        console.log(this.responseText);
        document.querySelector('#body').innerHTML = response;
    
        // Push state to URL
        //document.title = name;
        //history.pushState(null, name, name);
    };
    request.send(params);
}

function myrefresh() {
    window.location.reload();
}

function create_table(id, ip, addr, num, d1temp, d2temp, d3temp, status) {
    var overview_table = document.getElementById("dashboard");
    var row = overview_table.insertRow(-1);
    var cell_id = row.insertCell(0);
    var cell_ip = row.insertCell(1);
    var cell_addr = row.insertCell(2);
    var cell_num = row.insertCell(3);
    //var cell_time = row.insertCell(4);
    var cell_d1temp = row.insertCell(4);    
    var cell_d2temp = row.insertCell(5);
    var cell_d3temp = row.insertCell(6);
    var cell_status = row.insertCell(7);
    var elm1 = document.createElement("span");
    var elm2 = document.createElement("span");
    var elm3 = document.createElement("span");
    var elm4 = document.createElement("span");
    
    if (d1temp >= 75) {
        elm1.innerHTML = d1temp;
        elm1.classList.add("overheating");
    } else if (d1temp < 75 && d1temp > 65) {
        elm1.innerHTML = d1temp;
        elm1.classList.add("overload");
    } else {
        elm1.innerHTML = d1temp;
        elm1.classList.add("standard");
    }
    
    if (d2temp >= 75) {
        elm2.innerHTML = d2temp;
        elm2.classList.add("overheating");
    } else if (d2temp < 75 && d2temp > 65) {
        elm2.innerHTML = d2temp;
        elm2.classList.add("overload");
    } else {
        elm2.innerHTML = d2temp;
        elm2.classList.add("standard");
    }
    
    if (d3temp >= 75) {
        elm3.innerHTML = d3temp;
        elm3.classList.add("overheating");
    } else if (d3temp < 75 && d3temp > 65) {
        elm3.innerHTML = d3temp;
        elm3.classList.add("overload");
    } else {
        elm3.innerHTML = d3temp;
        elm3.classList.add("standard");
    }
    
    if (status === "Great") {
        elm4.innerHTML = status;
        elm4.classList.add("standard");
    } else {
        elm4.innerHTML = status;
        elm4.classList.add("overheating");
    }
    
    cell_id.innerHTML = id;
    cell_ip.innerHTML = ip;
    cell_addr.innerHTML = addr;
    cell_num.innerHTML = num;
    //cell_time.innerHTML = time;
    cell_d1temp.innerHTML = '';
    cell_d2temp.innerHTML = '';
    cell_d3temp.innerHTML = '';
    cell_status.innerHTML = '';
    
    cell_d1temp.appendChild(elm1);
    cell_d2temp.appendChild(elm2);
    cell_d3temp.appendChild(elm3);
    cell_status.appendChild(elm4);
    //console.log(cell_d1temp);
}

function load_dashboard() {
    var request = new XMLHttpRequest();
    request.open('GET', '/dashboard');
    request.onload = () => {
        const response = request.responseText;
        //console.log(response);
        var obj = JSON.parse(response);
        //console.log(obj);
        
        for (i=0; i< obj.length; i++) {
            //create_table(`${i+1}`, obj[i]['ip'], obj[i]['macaddress'], obj[i]['update_time'], 'D1: '+ obj[i]['temperture']['dt1_temperture'] + '℃' + ' ' + 'D2: ' + obj[i]['temperture']['dt2_temperture'] + '℃' + ' ' + 'D3: ' + obj[i]['temperture']['dt3_temperture'] + '℃');
            create_table(`${i+1}`, obj[i]['ip'], obj[i]['macaddress'], obj[i]['worker_num'], obj[i]['temperture']['dt1_temperture'], obj[i]['temperture']['dt2_temperture'], obj[i]['temperture']['dt3_temperture'], obj[i]['cond']);
        }
    };
    request.send();
}

document.addEventListener('DOMContentLoaded', () => {        
    load_dashboard();
    //setTimeout('myrefresh()',60000);
});
