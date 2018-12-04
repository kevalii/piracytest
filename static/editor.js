$(document).ready(function(){
	$('button').click(function(){
		getActiveText($(this).val())
		});
});

function getActiveText(arg)
{
	// Derivative of first solution to https://stackoverflow.com/questions/5379120/get-the-highlighted-selected-text
	var text = '';
	var activeText = $('#translation_text')
	var activeTag = activeText.prop('tagName');

	// Get selected text in textarea
	text = activeText.val().slice(activeText[0].selectionStart, activeText[0].selectionEnd);
	
	if (text == '')
	{
		arg = ''
	}

	beforeActiveText = activeText.val().slice(0, activeText[0].selectionStart);
	afterActiveText = activeText.val().slice(activeText[0].selectionEnd);
	switch(arg)
	{
		case 'bold':
			text = boldify(text);
			break;
		case 'italics':
			text = italicize(text)
			break;
		case 'underline':
			text = underline(text)
			break;
		default:
			break;
	}
	activeText.val(beforeActiveText + text + afterActiveText);
}

// Modifying functions
function boldify(text)
{
	return '<b>' + text + '</b>';
}

function italicize(text)
{
	return '<em>' + text + '</em>'
}

function underline(text)
{
	return '<u>' + text + '</u>'
}
