var projects = null;
$.ajax({
  crossOrigin:true,
  url:"http://127.0.0.1:5000/counter",
  datatype:"json",
  async:false,
  success:function(data){
      projects = data;
  }
});
console.log(projects);
