function menu_rename(event, ui) {
    var node = $.ui.fancytree.getNode(ui.target);
    if ((node.extraClasses || '').indexOf('root') != -1) {
        alert('Root node can not be renamed');
        return;
    }
    var title = node.title;
    var new_title = prompt('Rename', title);
    if (new_title != null)
        node.setTitle(new_title);
}

function menu_delete(event, ui) {
    var node = $.ui.fancytree.getNode(ui.target);
    if ((node.extraClasses || '').indexOf('root') != -1) {
        alert('Root node can not be removed');
        return;
    }
    node.remove();
}

function menu_add_folder(event, ui) {
    var node = $.ui.fancytree.getNode(ui.target);
    var title = prompt('Folder name', '');
    if (title != null)
        node.addChildren({
            title: title,
            folder: true
        });
}

function menu_add_item(event, ui) {
    var node = $.ui.fancytree.getNode(ui.target);
    var title = prompt('Item name', '');
    node.addChildren({
        title: title,
        folder: false
    });
}

function is_src_node(node) {
    return (node.extraClasses || '').indexOf('src-node') > -1;
}


function set_target_class(node) {
    node.visit(function(n) {
        n.addClass('target-node');
    });
}


function expand_tree(selector) {
    $(selector).fancytree("getRootNode").visit(function(node) {
        node.setExpanded(true);
    });
}

function message(text) {
    $('#message').html(text);
    $('#message').dialog();
}


var dnd = {
    draggable: {
        scroll: false
    },
    autoExpandMS: 400,
    focusOnClick: true,
    preventVoidMoves: true, // Prevent dropping nodes 'before self', etc.
    preventRecursiveMoves: true, // Prevent dropping nodes on own descendants
    dragStart: function(node, data) {
        return true;
    },

    dragEnter: function(node, data) {
        return true;
    },
    dragOver: function(node, data) {

        /* No DnD within the src tree */
        if (is_src_node(node) && is_src_node(data.otherNode)) {
            return false;
        }

        /** data.otherNode may be null for non-fancytree droppables.
         *  Return false to disallow dropping on node. In this case
         *  dragOver and dragLeave are not called.
         *  Return 'over', 'before, or 'after' to force a hitMode.
         *  Return ['before', 'after'] to restrict available hitModes.
         *  Any other return value will calc the hitMode from the cursor position.
         */
        // Prevent dropping a parent below another parent (only sort
        // nodes under the same parent)
        /*
            if(node.parent !== data.otherNode.parent){
                return false;
            }
            // Don't allow dropping *over* a node (would create a child)
            return ["before", "after"];
        */
        return true;
    },
    dragDrop: function(target_node, data) {
        var new_node = null;
        var source_node = data.otherNode;
        var source_class = (source_node.extraClasses || '').indexOf('src-node') > -1 ? 'src' : 'target';
        var target_class = (target_node.extraClasses || '').indexOf('src-node') > -1 ? 'src' : 'target';
        console.log(source_class);
        console.log(target_class);
        if (data.hitMode == 'over' && !target_node.folder) {
            message('Nodes can only be dropped on folders');
            return false;
        }
        if (source_class == 'src' && target_class == 'target') {
            new_node = data.otherNode.copyTo(target_node, data.hitMode);
            new_node.removeClass('src-node');
            set_target_class(data.otherNode);
            target_node.setExpanded(true);
        } else if (source_class == 'target' && target_class == 'target') {
            /* DnD 'over' only on folder nodes */
            new_node = data.otherNode.moveTo(target_node, data.hitMode);
            target_node.setExpanded(true);
        } else if (source_class == 'src' && target_class == 'src') {
            message('Can not move nodes within the source tree');
            return false;
        } else {
            message('Can not move nodes from target to source');
            return false;
        }
    }
}

$(document).ready(function() {

    $("#tree1").fancytree({
        extensions: ["dnd"],
        dnd: dnd,
        lazyLoad: function(event, data){
            var node = data.node;
            data.result = {
                url: CONNECTOR_URL + "/get_tree_data",
                data: {mode: "children", path: node.data.path},
                cache: false
            };
        },
    });

    $("#tree2").fancytree({
        extensions: ["dnd", "edit"],
        dnd: dnd
    });

    $("#tree2").contextmenu({
        delegate: "span.fancytree-title",
        menu: [{
            title: "Rename",
            cmd: "cut",
            uiIcon: "ui-icon-pencil",
            action: menu_rename
        }, {
            title: "Delete",
            cmd: "delete",
            uiIcon: "ui-icon-trash",
            action: menu_delete
        }, {
            title: "Add item",
            cmd: "Add item",
            uiIcon: "ui-icon-document",
            action: menu_add_item
        }, {
            title: "Add folder",
            cmd: "Add folder",
            uiIcon: "ui-icon-folder-collapsed",
            action: menu_add_folder
        }, ],
        beforeOpen: function(event, ui) {
            var node = $.ui.fancytree.getNode(ui.target);
        },
    });

    expand_tree('#tree1');
    expand_tree('#tree2');

});
