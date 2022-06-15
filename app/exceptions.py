from fastapi import HTTPException, status

CategoryAlreadyRegistered = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Category already registered',
)

CharacteristicAlreadyRegistered = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Characteristic already registered',
)

CategoryNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Category Not Found',
)

CharacteristicNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Characteristic Not Found',
)

ProductNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Product Not Found',
)

DuplicateCharacteristic = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='You stated the same characteristic several times',
)

ProductAlreadyRegistered = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='This SKU already registered',
)

WrongPrice = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='The price has to be positive',
)

InsufficientStock = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Not enough items in stock',
)

OrderNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Order Not Found',
)

OrderNotPaid = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='The order not paid yet',
)

OrderAlreadyCompleted = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='The order is already completed',
)
