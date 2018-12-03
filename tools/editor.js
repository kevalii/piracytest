function getActiveText()
{
	// derivative of first solution to https://stackoverflow.com/questions/5379120/get-the-highlighted-selected-text
	var text = '';
	var activeText = $(document.activeElement);
	var activeTag = activeText.prop('tagName');

	// make sure that selected element is within textarea
	if (activeText == $('#translation_text'))
	{
		text = activeText.val().slice(activeText.selectionStart, activeText.selectionEnd);
	}
	return text;
}

// potential switch statement?
function boldify()
{
	return '<b>' + getActiveText() + '</b>';
}

function italicize()
{
	return '<em>' + getActiveText() + '</em>'
}
