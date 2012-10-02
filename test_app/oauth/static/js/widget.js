function widget(id, url){
    var hheader = ['name', 'kind', 'created', 'updated'];
    function init(){
        var thead = $('<thead></thead>').append();
        var tr = $('<tr></tr>');
        for(var a=0; a < hheader.length; ++a){
            var th = $('<th></th>').attr('scope','col').text(hheader[a].charAt(0).toUpperCase() + hheader[a].slice(1));
            tr.append(th);
        }
        var table = $('<table></table>').append(thead.append(tr)).attr('id',id).append($('<tbody></tbody>'));
        table.data('widget_data_' + id);
        return table;
    }
    function updateData(element, data){
        var current_data = element.data('widget_data_' + id);
        $.extend(true, current_data, data);
        element.data('widget_data_' + id, data);
    }
    function refreshData(data){
        updateData(element, data);
        console.log(data);
        /*
        element.children('tbody').find('tr').remove();
        for(var a=0; a < data.items.length; ++a){
            var tr = $('<tr></tr>');
            for(var b=0; b < hheader.length; ++b){
                tr.append($('<td></td>').text(data.items[a][hheader[b]]));
            }
            element.append(tr);
        }
        */
    }
    function fetchData(){
        $.get(url, function(dd){refreshData(dd)}, 'json');
    }
    function startInterval(fn, seconds){
        setInterval(function(){fn();},seconds*1000);
    }
    var element = init();
    fetchData();
    startInterval(fetchData, 5);
    return element;
}