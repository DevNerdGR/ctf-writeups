# Information
- **CTF:** *TJCTF*
- **Challenge name:** *guess-again*
- **Challenge description:** *What happens if you press the button?*
- **Category:** *rev*
- **Date:** *June 2025*
# Approach
We are provided with an Excel file, that when opened, warns us about potential security issues due to the presence of macros.

Macros are essentially small scripts that users can in Excel to automate certain tasks. They can be very powerful (and dangerous too)!

By changing the security permissions of the file, we are able to view the macros present:
```vb
Sub CheckFlag()
    Dim guess As String
    guess = ActiveSheet.Shapes("TextBox 1").TextFrame2.TextRange.Text

    If Len(guess) < 7 Then
        MsgBox "Incorrect"
        Exit Sub
    End If

    If Left(guess, 6) <> "tjctf{" Or Right(guess, 1) <> "}" Then
        MsgBox "Flag must start with tjctf{ and end with }"
        Exit Sub
    End If

    Dim inner As String
    inner = Mid(guess, 7, Len(guess) - 7)
    
    Dim expectedCodes As Variant
    expectedCodes = Array(98, 117, 116, 95, 99, 52, 110, 95, 49, 116, 95, 114, 117, 110, 95, 100, 48, 48, 109)
    Dim i As Long
    If Len(inner) <> (UBound(expectedCodes) - LBound(expectedCodes) + 1) Then
        MsgBox "Incorrect"
        Exit Sub
    End If
    For i = 1 To Len(inner)
        If Asc(Mid(inner, i, 1)) <> expectedCodes(i - 1) Then
            MsgBox "Incorrect"
            Exit Sub
        End If
    Next i
    
    MsgBox "Flag correct!"
End Sub
    


Function check(str, arr, idx1, idx2) As Boolean
    If Mid(str, idx1, 1) = Chr(arr(idx2)) Then
        check = True
    Else
        check = False
End Function
```

Scanning through the code, it seems that the `CheckFlag()` function is called when the button is pressed. `CheckFlag()` reads in user input in the text box then checks if the flag is correct.

Not being very familiar with visual basic (the programming language used for writing macros), instead of trying to parse the code to work out what it does, I noticed the variable `expectedCodes` contained an array of integers. These integers all seem to be within printable ASCII range.

Copying out the array and then pasting it in python and running some conversion code, we get the following output:
```
>>> "".join(chr(x) for x in [98, 117, 116, 95, 99, 52, 110, 95, 49, 116, 95, 114, 117, 110, 95, 100, 48, 48, 109])
'but_c4n_1t_run_d00m'
```

If we look slightly before this array, we notice that there is already some code to check that the input starts with `trjctf{` and ends with `}`. Hence, the assembled flag is probably `tjctf{but_c4n_1t_run_d00m}`.

Indeed, if we enter this into the textbox and click on the 'Check Flag' button, we are greeted by a popup indicating that our flag is indeed correct!
# Flag
```tjctf{but_c4n_1t_run_d00m}```
# Tags
- TJCTF
- Rev
- Visual Basic
- Excel
- Macros
---
*Written on 09-06-2025*

