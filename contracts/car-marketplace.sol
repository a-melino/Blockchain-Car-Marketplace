// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract CarMarketplace is ERC721Full {

    constructor() public ERC721Full("CarToken", "CAR") {}

    struct Car {
        string brand;
        string model;
        uint256 year;
        uint256 kilometers;
        string fuelType;
        string engine;
        string transmission;
        uint256 accident;
        uint256 cleanTitle;
        uint256 price;
        bool isForSale;
        string carJson;
    }

    mapping (uint256 => Car) public carCollection;

    event CarListedForSale(uint256 indexed tokenId, uint256 price, address indexed seller);

    event CarSold(uint256 indexed tokenId, address indexed seller, address indexed buyer, uint256 price);

    function getCarDetails(uint256 tokenId) public view returns (string memory detailsJson) {
        return carCollection[tokenId].carJson;
    }

    function registerCar(
        address ownerAddress, 
        Car memory newCar,
        string memory carURI
    ) public returns (uint256) {

        uint256 tokenId = totalSupply();
        _mint(ownerAddress, tokenId);
        _setTokenURI(tokenId, carURI);

        carCollection[tokenId] = newCar;

        return tokenId;
    }

    function listCarForSale(uint256 tokenId, uint256 price) public {
        // Check if the caller is the owner of the car
        require(ownerOf(tokenId) == msg.sender, "You are not the owner of this car.");
        
        // Update the car's sale status and set the sale price
        carCollection[tokenId].isForSale = true;
        carCollection[tokenId].price = price;
        
        // Emit an event to log the listing of the car for sale
        emit CarListedForSale(tokenId, price, msg.sender);
    }



    function purchaseCar(uint256 tokenId) public payable {
        // Check if the car is listed for sale
        require(carCollection[tokenId].isForSale, "Car is not listed for sale.");

        // Check if the buyer has sent enough Ether to purchase the car
        require(msg.value >= carCollection[tokenId].price, "Insufficient funds to purchase the car.");

        // Store the current owner's address
        address currentOwner = ownerOf(tokenId);

        // Transfer the purchase funds to the current owner
        address payable seller = address(uint160(currentOwner));
        seller.transfer(msg.value);

        // Transfer ownership of the car token to the buyer
        _transferFrom(currentOwner, msg.sender, tokenId);

        // Update car listing status (no longer for sale)
        carCollection[tokenId].isForSale = false;

        // Emit an event to log the sale
        emit CarSold(tokenId, currentOwner, msg.sender, msg.value);
    }

}
