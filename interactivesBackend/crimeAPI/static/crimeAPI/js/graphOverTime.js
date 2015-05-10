var Graph1 = {
  INCREMENT_NUM_HOURS: 24,

  RATIO: 5/6,
  graph1: null,
  MARGIN: {top: 20, right: 30, bottom: 120, left: 60},
  yScaler: null,
  yAxis: null,
  xScaler: null,
  xAxis: null,
  tip: null,

  getWidthsAndHeights: function() {
    var width = parseInt(d3.select("#graph1Container").style("width"));
    var height = this.RATIO * width;
    var inner_width = width - this.MARGIN.left - this.MARGIN.right;
    var inner_height = height - this.MARGIN.top - this.MARGIN.bottom;
    return {width: width,
            height: height,
            inner_height: inner_height,
            inner_width: inner_width};
  },

  setupGraph: function() {
    var wAndH = this.getWidthsAndHeights();    

    // add tooltips
    this.tip = d3.tip()
    .attr('class', 'graph-tip')
    .html(function(d) { return "<strong>Count:</strong> <span style='color:#f03b20'>" + d.count + "</span>"; });

    this.graph1 = d3.select("#graph1")
                    .attr("width", wAndH.width)
                    .attr("height", wAndH.height)
                  .append("g")
                    .attr("transform", 
                          "translate(" + this.MARGIN.left 
                            + "," + this.MARGIN.top + ")")
                    .call(this.tip);
    this.yScaler = d3.scale.linear()
                  .range([wAndH.inner_height, 0]);
  },

  drawGraph: function(start, end, increment, data) {
    var wAndH = this.getWidthsAndHeights();
    var inner_width = wAndH.inner_width;
    var inner_height = wAndH.inner_height;

    var currentData = [];
    var currentDay = start;

    // fill currentData with objects with date and count attributes
    // *** doesn't include the first day ***
    for (var i = 0; i < data.length; i++) {
      currentData.push({
                        count: data[i].number,
                        date: currentDay.setHours(currentDay.getHours() + increment)
                      });
    };

    // make y-axis
    this.yScaler = this.yScaler
            .domain([0, d3.max(data, function(d) { return d.number; })]);

    this.yAxis = d3.svg.axis()
    .scale(this.yScaler)
    .ticks(11)
    .orient("left");

    // if the max value is 9, set ticks so there are no decimals
    if (d3.max(currentData, function(d) { return d.count; }) <= 9) {
     this.yScaler = d3.scale.linear()
              .range([inner_height, 0])
              .domain([0, 9]);

      this.yAxis = d3.svg.axis()
      .scale(this.yScaler)
      .tickValues([0,1,2,3,4,5,6,7,8,9])
      .orient("left");
    };

    // get rid of pre-existing y-axis
    this.graph1.select(".yAxis").remove();

    this.graph1.append("g")
         .attr("class", "yAxis")
         .call(this.yAxis)
      .append("text")
         .attr("transform", "rotate(-90)")
         .attr("x", -(wAndH.inner_height / 2))
         .attr("y", -100)
         .attr("dy", "4em")
         .style("text-anchor", "end")
         .text("Count");

    // make x-axis
    this.xScaler = d3.scale.ordinal() 
        .rangeRoundBands([0, inner_width], .1)
        .domain(currentData.map(function(d) { return d.date; }));

    this.xAxis = d3.svg.axis()
    .scale(this.xScaler) 
    .tickFormat(function (d) {
      var months = ["Jan", "Feb", "March", "April", "May", "June", "July",
                    "Aug", "Sep", "Oct", "Nov", "Dec"];
      var date = new Date(d); 
      return [months[date.getMonth()],
                     date.getDate() + ",",
                     date.getFullYear()].join(" ");})
    .orient("bottom");

    // add bars
    var selection = this.graph1.selectAll(".bar")
                    .data(currentData);

    var selectionEnter = selection
                          .enter();

    // get rid of pre-existing x-axis
    this.graph1.select(".xAxis").remove();

    selectionEnter.append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return this.xScaler(d.date); }.bind(this))
            .attr("y", function(d) { return this.yScaler(d.count); }.bind(this))
            .attr("height", function(d) { return inner_height - this.yScaler(d.count); }.bind(this))
            .attr("width", this.xScaler.rangeBand())
            .on("mouseover", this.tip.show.bind(this))
            .on("mouseout", this.tip.hide);
    this.graph1.append("g")
            .attr("class", "xAxis")
            .attr("transform", "translate(0," + inner_height + ")")
            .call(this.xAxis)
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                return "rotate(-65)" 
                });

    // update bars
    selection
          .attr("class", "bar")
          .attr("x", function(d) { return this.xScaler(d.date); }.bind((this)))
          .attr("y", function(d) { return this.yScaler(d.count); }.bind(this))
          .attr("height", function(d) { return inner_height - this.yScaler(d.count); }.bind(this))
          .attr("width", this.xScaler.rangeBand());

    // clear graph for next set of bars
    selection.exit().remove();

  },
  
  display: function(start, end, catID) {

    reqMaker.crime_count_increment(this.INCREMENT_NUM_HOURS, start, 
                                   end, null, catID, null, 
                                   this.drawGraph.bind(this, start, end, this.INCREMENT_NUM_HOURS));
  },

  resize: function() {

    if (!this.yAxis) return; // drawGraph hasn't been run yet
    var wAndH = this.getWidthsAndHeights();
    d3.select("#graph1")
      .attr("width", wAndH.width)
      .attr("height", wAndH.height);

    this.yScaler = this.yScaler.range([wAndH.inner_height, 0])
    this.yAxis = this.yAxis
                .scale(this.yScaler);

    this.graph1.select(".yAxis").remove();

    this.graph1.append("g")
         .attr("class", "yAxis")
         .call(this.yAxis)
      .append("text")
         .attr("transform", "rotate(-90)")
         .attr("x", -(wAndH.inner_height / 2))
         .attr("y", -100)
         .attr("dy", "4em")
         .style("text-anchor", "end")
         .text("Count");

    this.xScaler = this.xScaler
              .rangeRoundBands([0, wAndH.inner_width], .1);

    this.xAxis = this.xAxis.scale(this.xScaler);

    this.graph1.select(".xAxis").remove();

    this.graph1.append("g")
            .attr("class", "xAxis")
            .attr("transform", "translate(0," + wAndH.inner_height + ")")
            .call(this.xAxis)
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                return "rotate(-65)" 
                });
    d3.selectAll("#graph1 .bar")
            .attr("x", function(d) { return this.xScaler(d.date); }.bind({xScaler:this.xScaler}))
            .attr("y", function(d) { return this.yScaler(d.count); }.bind({yScaler:this.yScaler}))
            .attr("height", function(d) { return this.inner_height - this.yScaler(d.count); }.bind({inner_height:wAndH.inner_height,
                                                                                                  yScaler:this.yScaler}))
            .attr("width", this.xScaler.rangeBand());
  }
}

$().ready(function () {
    var theGraphObjectTime = Object.create(Graph1);
    theGraphObjectTime.setupGraph();
    missionControl.addClient(theGraphObjectTime.display.bind(theGraphObjectTime));
    d3.select(window).on('resize.graphOverTime', theGraphObjectTime.resize.bind(theGraphObjectTime));
});
