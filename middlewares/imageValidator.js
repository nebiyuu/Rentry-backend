import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const validateImages = async (req, res, next) => {
  try {
    if (!req.files || req.files.length === 0) {
      return next();
    }

    const microserviceUrl = process.env.MICROSERVICE_URL || 'http://localhost:8000';
    const validationResults = [];

    for (const file of req.files) {
      try {
        const response = await fetch(`${microserviceUrl}/validate-image/?path=${encodeURIComponent(file.path)}`, {
          method: 'GET',
        });

        if (!response.ok) {
          throw new Error(`Validation service responded with status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Image validation result:', result);
        
        if (!result.valid) {
          // Clean up the temporary file if validation fails
          if (fs.existsSync(file.path)) {
            fs.unlinkSync(file.path);
          }
          
          return res.status(400).json({
            success: false,
            message: `Image validation failed for ${file.originalname}`,
            reason: result.reason,
            score: result.score
          });
        }

        validationResults.push({
          filename: file.originalname,
          valid: true,
          blur_score: result.blur_score,
          brightness_score: result.brightness_score
        });

      } catch (validationError) {
        // Clean up the temporary file if validation error occurs
        if (fs.existsSync(file.path)) {
          fs.unlinkSync(file.path);
        }
        
        return res.status(500).json({
          success: false,
          message: `Error validating image ${file.originalname}`,
          error: validationError.message
        });
      }
    }

    // Attach validation results to request for logging/debugging
    req.imageValidationResults = validationResults;
    next();

  } catch (error) {
    // Clean up all temporary files if a general error occurs
    if (req.files && req.files.length > 0) {
      req.files.forEach(file => {
        if (fs.existsSync(file.path)) {
          fs.unlinkSync(file.path);
        }
      });
    }

    return res.status(500).json({
      success: false,
      message: 'Image validation process failed',
      error: error.message
    });
  }
};

export { validateImages };
