function diagonalDifference(arr) {
    // Write your code here
    const n= arr.length
    let SumaDiagonalPrincipal =  0
    let  SumaDiagonalSecundaria = 0             
    for (let i = 0 ; i < n; i++){
    console.log(n, i)
     SumaDiagonalPrincipal += arr[i][i];
     SumaDiagonalSecundaria += arr[i][n - 1 - i];    
    }    
    
console.log( Math.abs(SumaDiagonalPrincipal - SumaDiagonalSecundaria))

}

diagonalDifference([
    [11, 2, 4],
    [4, 5, 6],
    [10, 8, -12]
]);