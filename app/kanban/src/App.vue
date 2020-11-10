<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col form">
        <b-form-input
          v-model="newTask"
          required
          placeholder="Task name"
          @keyup.enter="add"
          style="width: 300px;"
        ></b-form-input>
        <b-form-textarea
          v-model="newDetail"
          placeholder="Task detail"
          style="width: 300px; margin-top: 10px;"
        >
        </b-form-textarea>

        <b-button 
          @click="add" 
          variant="primary"
          style="margin-top: 10px;"
        >Create</b-button>

      </div>
    </div>
    <div class="row mt-5">
      <div class="col-3">
        <div class="p-2 alert alert-secondary">
          <h3>Back Log</h3>
          <!-- Backlog draggable component. Pass arrBackLog to list prop -->
          <draggable
            class="list-group kanban-column"
            :list="arrTodo"
            @end="update"
            group="tasks"
          >
            <div
              class="list-group-item" style="margin-top: 15px;"
              v-for="element in arrTodo"
              :key="element.name"
            >
              <div class="text-right">{{ element.due_date }}</div>
              <h6 class="card-title">{{ element.name }}</h6> 
              <hr noshade>
              <p>
{{ element.detail }}
              </p>
            </div>
          </draggable>
        </div>
      </div>

      <div class="col-3">
        <div class="p-2 alert alert-primary">
          <h3>In Progress</h3>
          <!-- In Progress draggable component. Pass arrInProgress to list prop -->
          <draggable
            class="list-group kanban-column"
            :list="arrWIP"
            @end="update"
            group="tasks"
          >
            <div
              class="list-group-item"  style="margin-top: 15px;"
              v-for="element in arrWIP"
              :key="element.name"
            >
              <div class="text-right">{{ element.due_date }}</div>
              <h6 class="card-title">{{ element.name }}</h6> 
              <hr noshade>
              <p>
{{ element.detail }}
              </p>
            </div>
          </draggable>
        </div>
      </div>

      <div class="col-3">
        <div class="p-2 alert alert-warning">
          <h3>Testing</h3>
          <!-- Testing draggable component. Pass arrTested to list prop -->
          <draggable
            class="list-group kanban-column"
            :list="arrCheck"
            @end="update"
            group="tasks"
          >
            <div
              class="list-group-item" style="margin-top: 15px;"
              v-for="element in arrCheck"
              :key="element.name"
            >
              <div class="text-right">{{ element.due_date }}</div>
              <h6 class="card-title">{{ element.name }}</h6> 
              <hr noshade>
              <p>
{{ element.detail }}
              </p>
            </div>
          </draggable>
        </div>
      </div>

      <div class="col-3">
        <div class="p-2 alert alert-success">
          <h3>Done</h3>
          <!-- Done draggable component. Pass arrDone to list prop -->
          <draggable
            class="list-group kanban-column"
            :list="arrDone"
            @end="update"
            group="tasks"
          >
            <div
              class="list-group-item" style="margin-top: 15px;"
              v-for="element in arrDone"
              :key="element.name"
            >
              <div class="text-right">{{ element.due_date }}</div>
              <h6 class="card-title">{{ element.name }}</h6> 
              <hr noshade>
              <p>
{{ element.detail }}
              </p>
            </div>
          </draggable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//import draggable
import draggable from "vuedraggable";
export default {
  name: "kanban-board",
  components: {
    //import draggable as a component
    draggable
  },
  async created(){

    const response = await fetch("http://localhost:5000/v1/kanban/", {
      mode: 'cors',
      credentials: 'same-origin',
      redirect: 'follow',
      cache: 'no-cache',
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    /*
    .then(response => response.json())
    .then(data => (this.arrBacklog = data.todo));
    */
    console.log(response);
    const d = await response.json();
    this.arrTodo = d.todo;
    this.arrWIP = d.wip;
    this.arrCheck = d.check;
    this.arrDone = d.done;
    console.log("created");
    console.log(d);

  },
  data() {

    return {
      // for new tasks
      newTask: "",
      newDetail: "",
      // 4 arrays to keep track of our 4 statuses
      arrTodo: [],
      arrWIP: [],
      arrCheck: [],
      arrDone: []
    };
  },
  methods: {
    //add new tasks method
    add: async function() {
      if (this.newTask) {
        const ret = await fetch("http://localhost:5000/v1/kanban/", {
          mode: 'cors',
          credentials: 'same-origin',
          redirect: 'follow',
          cache: 'no-cache',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name: this.newTask, detail: this.newDetail })
        });
        const d = await ret.json();
        console.log({ name: this.newTask, detail: this.newDetail });
        console.log(d);
        this.arrTodo = d.todo;
        this.arrWIP = d.wip;
        this.arrCheck = d.check;
        this.arrDone = d.done;
        this.newTask = "";
        this.newDetail = "";
      }
    },
    update: async function(){
      console.log("Task moved !!! ");
      let data = {
        'todo' : this.arrTodo,
        'wip' : this.arrWIP,
        'check' : this.arrCheck,
        'done' : this.arrDone
      }
      console.log(data);

      const ret = await fetch("http://localhost:5000/v1/kanban/", {
          mode: 'cors',
          credentials: 'same-origin',
          redirect: 'follow',
          cache: 'no-cache',
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Request-Method': '*'
          },
          body: JSON.stringify(data)
      });
      const d = await ret.json();
      console.log(d);
      this.arrTodo = d.todo;
      this.arrWIP = d.wip;
      this.arrCheck = d.check;
      this.arrDone = d.done;

    }
  }
};
</script>

<style>
/* light stylings for the kanban columns */
.kanban-column {
  min-height: 300px;
}
</style>