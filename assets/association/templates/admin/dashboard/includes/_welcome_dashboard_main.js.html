{% load i18n %}
{% load assets_tags %}

    $('#dash_main').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: '{% trans "DashBoard" %}'
        },
        subtitle: {
            text: '{% trans "Global Yearly Breakdown" %}'
        },
		legend: {
			reversed: true,
			//align: 'right',
			//verticalAlign: 'top',
			//y: 100,
			//layout: 'vertical'
		},
        xAxis: {
            categories: [
                {% for m in month_names %} '{{ m }}', {% endfor %}
            ]
        },
        yAxis: {
            title: {
                text: '{% trans "Amount" %}'
            },

        stackLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold',
                                color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                                
                            },
                            formatter: function() {
                            return '<b>'+ Math.round(this.total*Math.pow(10,2))/Math.pow(10,2)+' €</b>'
                            },
                            
                            y: -10
                        
                        
                        },
        },
{% comment %}
            labels: {
                items: [{
                    html: '{% trans "Global Yearly Breakdown" %}',
                    style: {
                        left: '5px',
                        top: '8px',
                        color: 'black'
                    }
                }]
            },
{% endcomment %}

    tooltip: {
        shared: false,
        valueSuffix: ' €'
    },
                    
        plotOptions: {
            column: {
                stacking: 'normal',
                pointPadding: 0,
	            groupPadding: 0.1
            }
        },

        series: [
{% for key, values in results_earnings.items %}
        {
            type: 'column',
            name: '{{ key }}',
            stack: '{% trans "Earnings" %}',
            data: [ {% for res in values %} {{ res.amount_earning|intchart }}, {% endfor %} ],
            color: colors_earning[ {{ forloop.counter }} ]
            //color: '#69CD4B'
        },
{% endfor %}
{% for key, values in results_spendings.items %}
        {
            type: 'column',
            name: '{{ key }}',
            stack: '{% trans "Spendings" %}',
            data: [ {% for res in values %} {{ res.amount_spending|intchart }}, {% endfor %} ],
            color: colors_spending[ {{ forloop.counter }} ]
            //color: '#FF6F34'
        },
{% endfor %}
        {
                type: 'pie',
                name: '{% trans "Total Amount" %}',
                data: [{
                    name: '{% trans "Earnings" %}',
                    y: {{ total_earning|intchart }},
                    color: '#69CD4B'
                }, {
                    name: '{% trans "Spendings" %}',
                    y: {{ total_spending|intchart }},
                    color: '#FF6F34'
                }],
                center: [20, 10],
                size: 50,
                showInLegend: false,
                dataLabels: {
                    enabled: false
                }
        }
        ]
    });
