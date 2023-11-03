//  student registration and CRUD AIP Call
export const ApiCall = ()=>{
    let API_URL = 'http://127.0.0.1:8000/Admin/StudentList/'
    fetch(API_URL)
        .then(response => {
            return response.json()
        })
        .then(data =>{
            showData(data)
        })
}

export const showData = data =>{
    let std_table = document.getElementById('std_table')

    data.forEach(student => {
        std_table.innerHTML += `
            <tr>
                <td>${student.reg_no}</td>
                <td>${student.name}</td>
                <td>${student.department}</td>
                <td>${student.batch}</td>
            </tr>
        `
    });
}


ApiCall()