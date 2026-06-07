def linear_search(list, key):
    """
    線形探索（Linear Search）
    リストの先頭から順番に、目的の値（key）を探します。
    
    引数:
        list (list): 探索対象のリスト
        key (any): 探したい値
        
    戻り値:
        int: 見つかった場合はそのインデックス（位置）、見つからなければ -1 を返す
    """
    # enumerateを使って、インデックス(i)と要素(item)を同時に取得してループを回す
    for i, item in enumerate(list):
        if item == key:
            return i  # 目的の値が見つかったら、その位置を返す
            
    return -1  # リストを最後まで探しても見つからなかった場合


def binary_search(list, key):
    """
    二分探索（Binary Search）
    探索範囲を半分に分割しながら、目的の値（key）を探します。
    ※前提条件：リストがあらかじめソート（昇順に並び替え）されている必要があります。
    
    引数:
        list (list): 探索対象のリスト（ソート済みであること）
        key (any): 探したい値
        
    戻り値:
        int: 見つかった場合はそのインデックス（位置）、見つからなければ -1 を返す
    """
    left = 0                 # 探索範囲の左端のインデックス
    right = len(list) - 1    # 探索範囲の右端のインデックス

    # 左端が右端を追い越さない限り、探索を続ける
    while left <= right:
        middle = (left + right) // 2  # 探索範囲の中央のインデックスを計算
        
        if list[middle] == key:
            return middle  # 中央の値が目的の値だった場合、その位置を返す
            
        if list[middle] > key:
            # 中央の値よりも目的の値が小さい場合、目的の値は「左半分」にある
            right = middle - 1  # 探索範囲の右端を、中央の1つ左に狭める
            
        if list[middle] < key:
            # 中央の値よりも目的の値が大きい場合、目的の値は「右半分」にある
            left = middle + 1   # 探索範囲の左端を、中央の1つ右に狭める
            
    return -1  # 探索範囲がなくなっても見つからなかった場合
