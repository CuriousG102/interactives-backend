var Graph3 = {
  RATIO: 5/6,
  graph3: null,
  MARGIN: {top: 20, right: 30, bottom: 120, left: 60},
  yScaler: null,
  yAxis: null,
  xScaler: null,
  xAxis: null,
  tip: null,

  getWidthsAndHeights: function() {
    var width = parseInt(d3.select("#graph3Container").style("width"));
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

    this.graph3 = d3.select("#graph3")
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

  drawGraph: function(start, end, data) {
    var wAndH = this.getWidthsAndHeights();
    var inner_width = wAndH.inner_width;
    var inner_height = wAndH.inner_height;

    var currentData = [];
    for (var key in data) {
      if (data.hasOwnProperty(key) && key != "") {
        var areaObject = {
          name: key,
          count: data[key]
        };
        currentData.push(areaObject);
      }
    };

    // make y-axis
    this.yScaler = d3.scale.linear()
            .range([inner_height, 0])
            .domain([0, d3.max(currentData, function(d) { return d.count; })]);

    this.yAxis = d3.svg.axis()
    .scale(this.yScaler)
    .ticks(11)
    .orient("left");

    // if the max value is 9, set ticks so there are no decimals
    if ( d3.max(currentData, function(d) { return d.count; }) <= 9) {
      this.yScaler = d3.scale.linear()
              .range([inner_height, 0])
              .domain([0, 9]);

      this.yAxis = d3.svg.axis()
      .scale(this.yScaler)
      .tickValues([0,1,2,3,4,5,6,7,8,9])
      .orient("left");
    };

    // get rid of pre-existing y-axis
    this.graph3.select(".yAxis").remove();

    this.graph3.append("g")
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
        .domain(currentData.map(function(d) { return d.name; }));

    this.xAxis = d3.svg.axis()
    .scale(this.xScaler) 
    .orient("bottom");

    // add bars
    var selection = this.graph3.selectAll(".bar")
                    .data(currentData);

    var selectionEnter = selection
                          .enter();

    // get rid of pre-existing x-axis
    this.graph3.select(".xAxis").remove();

    selectionEnter.append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return this.xScaler(d.name); }.bind(this))
            .attr("y", function(d) { return this.yScaler(d.count); }.bind(this))
            .attr("height", function(d) { return inner_height - this.yScaler(d.count); }.bind(this))
            .attr("width", this.xScaler.rangeBand())
            .on("mouseover", this.tip.show.bind(this))
            .on("mouseout", this.tip.hide);
    this.graph3.append("g")
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
          .attr("x", function(d) { return this.xScaler(d.name); }.bind(this))
          .attr("y", function(d) { return this.yScaler(d.count); }.bind(this))
          .attr("height", function(d) { return inner_height - this.yScaler(d.count); }.bind(this))
          .attr("width", this.xScaler.rangeBand());

    // clear graph for next set of bars
    selection.exit().remove();

  },
  
  display: function(start, end, catID) {

    reqMaker.crime_count_area(start, end, null, catID, 
                                this.drawGraph.bind(this, start, end));
  },

  resize: function() {
    if (!this.yAxis) return; // drawGraph hasn't been run yet
    var wAndH = this.getWidthsAndHeights();
    d3.select("#graph3")
      .attr("width", wAndH.width)
      .attr("height", wAndH.height);

    this.yScaler = this.yScaler.range([wAndH.inner_height, 0])
    this.yAxis = this.yAxis
                .scale(this.yScaler);

    this.graph3.select(".yAxis").remove();

    this.graph3.append("g")
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

    this.graph3.select(".xAxis").remove();

    this.graph3.append("g")
            .attr("class", "xAxis")
            .attr("transform", "translate(0," + wAndH.inner_height + ")")
            .call(this.xAxis)
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                return "rotate(-65)" 
                });;
    d3.selectAll("#graph3 .bar")
            .attr("x", function(d) { return this.xScaler(d.name); }.bind({xScaler:this.xScaler}))
            .attr("y", function(d) { return this.yScaler(d.count); }.bind({yScaler:this.yScaler}))
            .attr("height", function(d) { return this.inner_height - this.yScaler(d.count); }.bind({inner_height:wAndH.inner_height,
                                                                                                  yScaler:this.yScaler}))
            .attr("width", this.xScaler.rangeBand());
  }
}

$().ready(function () {
    var theGraphObjectArea = Object.create(Graph3);
    theGraphObjectArea.setupGraph();
    missionControl.addClient(theGraphObjectArea.display.bind(theGraphObjectArea));
    d3.select(window).on('resize.graphByArea', theGraphObjectArea.resize.bind(theGraphObjectArea));
});

