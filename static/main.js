window.onload = () => {
    const app = new App("root");
    app.getUsers();
};

class App {
    constructor(rootElementId) {
        this.users = [];
        this.rootNode = document.getElementById(rootElementId);
    }

    getUsers() {
        axios.get("/users/")
            .then(response => {
                this.users = response.data;
                this.showUsers();
            })
        .catch(error=> {
            console.log(error)
        })
    }
    showUsers() {
        if (this.users.length === 0){
            return null;
        }
        const tableElm = document.createElement("table");
        tableElm.setAttribute("border", "1");
        const caption = document.createElement("caption");
        caption.append("Cognito users");
        tableElm.append(caption);
        const trH = document.createElement("tr");
        const th1 = document.createElement("th");
        const th2 = document.createElement("th");
        const th3 = document.createElement("th");
        th1.append("id");
        th2.append("email");
        th3.append("status");
        trH.append(th1, th2, th3);
        tableElm.append(trH);
        this.rootNode.append(tableElm);
        this.users.forEach((user) => {
            const trElm = document.createElement("tr");
            const tdElm1 = document.createElement("td");
            const tdElm2= document.createElement("td");
            const tdElm3= document.createElement("td");
            tdElm1.append(user.Username);
            tdElm2.append(user.Email)
            tdElm3.append(user.UserStatus);
            trElm.append(tdElm1, tdElm2, tdElm3);
            tableElm.append(trElm);
        });

    }
}
